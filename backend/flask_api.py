import datetime

from quart import Quart, request, jsonify, Blueprint
import asyncio

from backend.api import cashflow_api as cAPI
from backend.api import config_api as cfgAPI

from backend.integrations import integrations as iAPI

api_routes = Blueprint('api_routes', __name__)

#   =================================================================
#   =================================================================


#   GET METHODS
@api_routes.route('/api/cashflow/get/intrari', methods=['POST'])
async def get_intrari():

    request_json = await request.get_json()
    print(request_json)

    raw_data = await cAPI.get_intrari(
            firma=request_json['firma'],
            luna=request_json['luna'],
            an=request_json['an'],
            only_urgent=request_json.get('onlyUrgents', False)
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}

    for entry in raw_data:
        id, tip, isUrgent, zi, luna, an, firma, suma, tva, total = entry

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firma", {})
        firme_zi[firma] = firme_zi.get(firma, {})

        firme_zi[firma]['sume'] = firme_zi[firma].get('sume', [])
        firme_zi[firma]['sume'].append(suma)
        firme_zi[firma]['isUrgent'] = isUrgent

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firma": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an,
            "hasUrgent": max([firme_zi[firma]['isUrgent'] for firma in firme_zi])
        }

    print(data)

    return jsonify(data)

@api_routes.route('/api/cashflow/get/iesiri', methods=['POST'])
async def get_iesiri():

    request_json = await request.get_json()
    print(request_json)

    raw_data = await cAPI.get_iesiri(
            firma=request_json['firma'],
            luna=request_json['luna'],
            an=request_json['an'],
            only_urgent=request_json.get('onlyUrgents', False)
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}
    hasUrgent = False

    for entry in raw_data:
        id, tip, isUrgent, zi, luna, an, firma, suma, tva, total = entry

        if isUrgent == 1:
            hasUrgent = True

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firma", {})
        firme_zi[firma] = firme_zi.get(firma, {})

        firme_zi[firma]['sume'] = firme_zi[firma].get('sume', [])
        firme_zi[firma]['sume'].append(suma)
        firme_zi[firma]['isUrgent'] = isUrgent

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firma": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an,
            "hasUrgent": hasUrgent
        }

    print(data)

    return jsonify(data)

@api_routes.route('/api/cashflow/get/recents', methods=['GET'])
async def get_recents():

    raw_data = await cAPI.get_recent_operations(
        limit=3
    )
    print(raw_data)

    data = []

    for entry in raw_data:
        id, tip, isUrgent, zi, luna, an, firma, suma, tva, total = entry

        data.append(
            {
                "zi": zi,
                "luna": luna,
                "an": an,
                "firma": firma,
                "suma": suma,
                "tip": tip,
                "isUrgent": isUrgent
            }
        )

    return jsonify(data)

@api_routes.route('/api/cashflow/get/date_lunare', methods=['POST'])
async def get_date_lunare():
    json_data = await request.get_json()

    raw_data = await cAPI.get_date_lunare(
        luna=json_data['luna'],
        an=json_data['an']
    )

    if len(raw_data) == 0:
        return jsonify({
            "suma_initiala": 0
        })

    return jsonify({
        "suma_initiala": raw_data[0]
    })

@api_routes.route('/api/cashflow/get/conturi', methods=['GET'])
async def get_conturi():
    raw_data = await cAPI.get_conturi_bancare()

    data = []

    for entry in raw_data:
        banca, sold = entry

        data.append(
            {
                "banca": banca,
                "sold": sold
            }
        )

    return jsonify(data)

@api_routes.route('/api/cashflow/get/angajati')
async def get_angajati():
    raw_data = await cAPI.get_angajati()

    data = [{
        "ID": ID,
        "nume": nume,
        "firma": firma
    } for ID, nume, firma in raw_data]

    return jsonify(data)

async def __get_angajati():
    # This is a private method, used to get the list of angajati
    # from the database
    raw_data = await cAPI.get_angajati()

    data = [{
        "ID": ID,
        "nume": nume,
        "firma": firma,
        "nrCtr": nrCtr,
        "functia": functia,
        "cnp": cnp,
        "ci": ci,
        "valabilitate": valabilitate,
        "fisaAptitudini": fisaAptitudini,
        "nrTelefon": nrTelefon,
        "iban": iban
    } for ID, nume, firma, nrCtr, functia, cnp, ci, valabilitate, fisaAptitudini, nrTelefon, iban in raw_data]

    return data


@api_routes.route('/api/cashflow/get/angajat/<int:id>')
async def get_angajat(id):
    raw_data = await cAPI.get_angajat(id)

    data = {
        "ID": raw_data[0],
        "nume": raw_data[1],
        "firma": raw_data[2]
    }

    return jsonify(data)

async def __get_angajat(id):
    # This is a private method, used to get the list of angajati
    # from the database
    raw_data = (await cAPI.get_angajat(id))[0]

    data = {
        "ID": raw_data[0],
        "nume": raw_data[1],
        "firma": raw_data[2]
    }

    return data

@api_routes.route('/api/cashflow/get/salariu', methods=['POST'])
async def get_salariu():
    json_data = await request.get_json()

    raw_data = await cAPI.get_salarii(
        an=json_data['an'],
        angajati= [json_data['angajatID']]
    )

    data = [
        {
            "luna": luna,
            "salariu": salariu,
            "bonus": bonus
        } for  _, luna, _, _, _, salariu, bonus in raw_data
    ]

    return jsonify(data)

async def __get_salariu(an, angajati):
    raw_data = await cAPI.get_salarii(
        an=an,
        angajati=angajati
    )

    print(raw_data)

    data = [
        {
            "luna": luna,
            "salariu": salariu,
            "bonus": bonus
        } for _, luna, _, _, _, salariu, bonus in raw_data
    ]

    return data


# Maybe UNUSED
@api_routes.route('/api/cashflow/get/salariiSum', methods=['POST'])
async def get_salarii_sum():
    json_data = await request.get_json()

    raw_data = await cAPI.get_salarii(
        an=json_data['an'],
        luna=json_data['luna']
    )
    print(raw_data)

    sum = 0
    for entry in raw_data:
        sum += entry[5]
        sum += entry[6]

    data = {
        "suma": sum
    }

    return jsonify(data)

@api_routes.route('/api/cashflow/get/inventarAngajat', methods=['POST'])
async def get_inventar():
    json_data = await request.get_json()

    raw_data = await cAPI.get_inventar_angajat(
        angajat=json_data['angajatID']
    )

    data = [{
        "nume": nume,
        "cantitate": cantitate,
        "valoare": valoare
    } for _, nume, cantitate, valoare, _ in raw_data]

    return jsonify(data)

async def __get_inventar(angajat):
    raw_data = await cAPI.get_inventar(
        id_angajat=[angajat]
    )

    data = [{
        "id": id,
        "nume": nume,
        "cantitate": cantitate,
        "valoare": valoare
    } for id, nume, cantitate, valoare, _ in raw_data]

    return data

@api_routes.route('/api/cashflow/get/flota', methods=['GET'])
async def get_flota():
    raw_data = await cAPI.get_flota()

    data = [{
        "ID": ID,
        "masina": masina,
        "nrInmatriculare": nrInmatriculare,
        "gps": gps,
        "serieSasiu": serieSasiu,
        "combustibil": combustibil,
        "itp": itp,
        "zileItp": datetime.datetime.strptime(itp, "%Y-%m-%d") - datetime.datetime.now(),
        "rca": rca,
        "zileRca": datetime.datetime.now() - datetime.datetime.now(),
        "rovinieta": rovinieta,
        "zileRovinieta": datetime.datetime.strptime(rovinieta, "%Y-%m-%d") - datetime.datetime.now(),
        "copieConforma": copieConforma,
        "zileConforma": datetime.datetime.strptime(copieConforma, "%Y-%m-%d") - datetime.datetime.now(),
        "sofer": sofer
    } for ID, masina, nrInmatriculare, gps, serieSasiu, combustibil, itp, zileItp, rca, zileRca, rovinieta, zileRovinieta, copieConforma, zileConforma, sofer in raw_data]

    return jsonify(data)

async def __get_flota():
    raw_data = await cAPI.get_flota()


    def ____get_translated_timedelta(
            date1: datetime.datetime,
            date2: datetime.datetime
    ):
        delta = date1 - date2
        return f'{delta.days} {abs(delta.days) != 1 and "zile" or "zi" }'

    data = [{
        "ID": ID,
        "masina": masina,
        "nrInmatriculare": nrInmatriculare,
        "gps": gps,
        "serieSasiu": serieSasiu,
        "combustibil": combustibil,
        "itp": itp,
        "zileItp": ____get_translated_timedelta(datetime.datetime.strptime(itp, "%Y-%m-%d"), datetime.datetime.now()),
        "rca": rca,
        "zileRca": ____get_translated_timedelta(datetime.datetime.strptime(rca, "%Y-%m-%d"), datetime.datetime.now()),
        "rovinieta": rovinieta,
        "zileRovinieta": ____get_translated_timedelta(datetime.datetime.strptime(rovinieta, "%Y-%m-%d"), datetime.datetime.now()),
        "copieConforma": copieConforma,
        "zileConforma": ____get_translated_timedelta(datetime.datetime.strptime(copieConforma, "%Y-%m-%d"), datetime.datetime.now()),
        "sofer": sofer
    } for ID, masina, nrInmatriculare, gps, serieSasiu, combustibil, itp, rca, rovinieta, copieConforma, sofer in raw_data]

    return data


#   =================================================================
#   =================================================================


#   POST METHODS
@api_routes.route('/api/cashflow/add/intrare', methods=['POST'])
async def add_intrare():
    return jsonify("Not implemented")

@api_routes.route('/api/cashflow/add/iesire', methods=['POST'])
async def add_iesire():
    ...

@api_routes.route('/api/cashflow/add/date_lunare', methods=['POST'])
async def add_date_lunare():
    json_data = await request.get_json()
    print(json_data)

    try:
        #   Get the current DateLunare for current time
        current_date_lunare = await cAPI.get_date_lunare(
            luna=json_data['luna'],
            an=json_data['an']
        )

        #   If there is no DateLunare for current time, create one
        #   TODO: Known Bug: multiple connections will be made to the database
        if len(current_date_lunare) == 0:
            await cAPI.insert_date_lunare(
                luna=json_data['luna'],
                an=json_data['an'],
                suma_initiala=json_data['suma_noua']
            )
        else:
            await cAPI.update_date_lunare(
                luna=json_data['luna'],
                an=json_data['an'],
                suma_initiala=json_data['suma_noua']
            )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/cont', methods=['POST'])
async def add_cont():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.insert_cont_bancar(
            banca=json_data['banca'],
            sold=json_data['sold']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/angajat', methods=['POST'])
async def add_angajat():
    json_data = await request.get_json()
    print(json_data)

    try:
        angajat = await cAPI.insert_angajat(
            nume=json_data['nume'],
            companii=[json_data['firma']],
            nrCtr=json_data['nrCtr'],
            functie=json_data['functie'],
            cnp=json_data['cnp'],
            ci=json_data['ci'],
            valabilitate=json_data['valabilitate'],
            fisaAptitudini=json_data['fisaAptitudini'],
            telefon=json_data['telefon'],
            iban=json_data['iban']
        )

        print(angajat)

        return jsonify({
            "status": "OK",
            "data": {
                "ID": angajat[1],
                "nume": json_data['nume'],
                "firma": json_data['firma'],
                "nrCtr": json_data['nrCtr'],
                "functie": json_data['functie'],
                "cnp": json_data['cnp'],
                "ci": json_data['ci'],
                "valabilitate": json_data['valabilitate'],
                "fisaAptitudini": json_data['fisaAptitudini'],
                "telefon": json_data['telefon'],
                "iban": json_data['iban']
            }
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/data', methods=['POST'])
async def add_date():
    json_data: list[dict] = await request.get_json()

    # Will get a JSON list like this:
    # [
    #   {
    #       "data": dd-mm-yyyy,
    #       "firma": "Company 1",
    #       "tip": "intrare",
    #       "valoare": "100",
    #   }
    # ]

    try:
        db_conn = cAPI.create_db_connection()

        for entry in json_data:
            date = entry['data']
            date = [int(x) for x in date.split('-')]

            firma = entry['firma']
            tip = entry['tip']
            valoare = float(entry['valoare'])
            urgent = entry['urgent']

            if tip == 'intrare':
                await cAPI.insert_intrare(
                    data=date,
                    companie=firma,
                    val=valoare,
                    tva=0,
                    total=valoare,
                    isUrgent=urgent,
                    db_connection=db_conn
                )
            elif tip == 'iesire':
                await cAPI.insert_iesire(
                    data=date,
                    companie=firma,
                    val=valoare,
                    tva=0,
                    total=valoare,
                    isUrgent=urgent,
                    db_connection=db_conn
                )

        db_conn.close()

        return jsonify({
            "status": "OK"
        })

    except Exception as e:
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/file', methods=['POST'])
async def add_file():
    files = await request.files
    form = await request.form

    try:
       if 'file' not in files:
           return jsonify({
               "status": "Error",
               "message": "No file found"
           })

       file = files['file']
       integration = form['integration']

       # Save the file to the server
       # Make the directory if it doesn't exist
       import os
       if not os.path.exists(f"__temp/{integration}"):
             os.makedirs(f"__temp/{integration}")

       await file.save(f"__temp/{integration}/{file.filename}")

       # Get the data from the file
       m_data = iAPI.integration(
           name=integration,
           file=f"__temp/{integration}/{file.filename}"
       )

       # Add the list to a json response
       body = {
            "status": "OK",
            "data": m_data
       }

       return jsonify(body)

    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/inventar', methods=['POST'])
async def add_inventar():
    json_data = await request.get_json()
    print(json_data)

    db_conn = cAPI.create_db_connection()

    try:
        for item in json_data:
            print(item)

            action = item['action']
            print(action)

            if action == 'add':
                await cAPI.insert_inventar(
                    id_angajat=item['id_angajat'],
                    nume=item['nume'],
                    cantitate=item['cantitate'],
                    valoare=item['valoare'],
                    db_connection=db_conn
                )
            elif action == 'update':
                await cAPI.update_inventar(
                    id_angajat=item['id_angajat'],
                    id_item=item['id_item'],
                    new_nume=item['nume'],
                    new_cantitate=item['cantitate'],
                    new_valoare=item['valoare'],
                    db_connection=db_conn
                )
            elif action == 'delete':
                await cAPI.delete_inventar(
                    id_angajat=item['id_angajat'],
                    id_item=item['id_item'],
                    db_connection=db_conn
                )

        db_conn.close()

        return jsonify({
            "status": "OK"
        })


    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/add/flota', methods=['POST'])
async def add_flota():
    json_data = await request.get_json()
    print(json_data)

    try:

        entry = await cAPI.insert_flota(
            masina=json_data['masina'],
            nrInmatriculare=json_data['nrInmatriculare'],
            gps=json_data['gps'],
            serieSasiu=json_data['serieSasiu'],
            combustibil=json_data['combustibil'],
            itp=json_data['itp'],
            rca=json_data['rca'],
            rovinieta=json_data['rovinieta'],
            copieConforma=json_data['copieComforma'],
            sofer=json_data['sofer']
        )

        print(entry)

        return jsonify({
            "status": "OK",
            "data": {
                "ID": entry[1],
                **json_data
            }
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })
#   =================================================================
#   =================================================================

#   UPDATE METHODS

@api_routes.route('/api/cashflow/update/contBancar', methods=['POST'])
async def update_cont():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.update_cont_bancar(
            banca=json_data['banca'],
            sold=json_data['sold']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })


@api_routes.route('/api/cashflow/update/salariat', methods=['POST'])
async def update_angajat():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.update_angajat(
            id=json_data['id'],
            data= {
                "Nume": json_data['nume'],
                "Companie": json_data['firma'],
                "NrCTR": json_data['nrCtr'],
                "Functie": json_data['functie'],
                "CNP": json_data['cnp'],
                "CI": json_data['ci'],
                "Valabilitate": json_data['valabilitate'],
                "FisaAptitudini": json_data['fisaAptitudini'],
                "Telefon": json_data['telefon'],
                "IBAN": json_data['iban']
            }
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/update/salariu', methods=['POST'])
async def update_salariu():
    json_data = await request.get_json()
    print(json_data)

    # Get the current salariu for the angajat
    salarii = await __get_salariu(
        an=json_data['an'],
        angajati=[json_data['angajatID']]
    )

    if len(salarii) > 0:
        method = cAPI.update_salariu
    else:
        method = cAPI.insert_salariu

    try:
        for salariu in json_data['salarii']:
            await method(
                luna=salariu['luna'],
                an=json_data['an'],
                id_angajat=json_data['angajatID'],
                companie=json_data['companie'],
                valoare=salariu['salariu'],
                bonus=salariu['bonus']
            )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/update/flota', methods=['POST'])
async def update_flota():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.update_flota(
            id=json_data['id'],
            data= {
                "Masina": json_data['masina'],
                "NrInmatriculare": json_data['nrInmatriculare'],
                "GPS": json_data['gps'],
                "SerieSasiu": json_data['serieSasiu'],
                "Combustibil": json_data['combustibil'],
                "ITP": json_data['itp'],
                "RCA": json_data['rca'],
                "Rovinieta": json_data['rovinieta'],
                "CopieConforma": json_data['copieComforma'],
                "Sofer": json_data['sofer']
            }
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

#   ================================================================
#   ===============================================================

#   DELETE METHODS
@api_routes.route('/api/cashflow/delete/intrare', methods=['POST'])
async def delete_intrare():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.delete_intrare(
            data=(int(json_data['zi']), int(json_data['luna']), int(json_data['an'])),
            companie=json_data['companie'],
            suma=json_data['suma']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/delete/iesire', methods=['POST'])
async def delete_iesire():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.delete_iesire(
            data=(int(json_data['zi']), int(json_data['luna']), int(json_data['an'])),
            companie=json_data['companie'],
            suma=json_data['suma']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/delete/contBancar', methods=['POST'])
async def delete_cont():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.delete_cont_bancar(
            banca=json_data['banca']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })


@api_routes.route('/api/cashflow/delete/salariat', methods=['POST'])
async def delete_angajat():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.delete_angajat(
            id=json_data['id']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })

@api_routes.route('/api/cashflow/delete/flota', methods=['POST'])
async def delete_flota():
    json_data = await request.get_json()
    print(json_data)

    try:
        await cAPI.delete_flota(
            id=json_data['id']
        )

        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "Error"
        })


#   =================================================================
#   =================================================================



#   TESTING METHODS
@api_routes.route('/api/test/cashflow/__createIesiri', methods=['GET'])
async def create_iesiri():
    await cAPI.create_cashflow_table()
    await cAPI.insert_iesire_many(
        entries=[
            [(1, 2, 2021), 'Company 2', 120, 19, 119],
            [(1, 2, 2021), 'Company 3', 24, 19, 238],
        ]
    )
    return "OK"
