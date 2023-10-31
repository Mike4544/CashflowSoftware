from quart import Quart, request, jsonify, Blueprint
import asyncio

from backend.api import cashflow_api as cAPI
from backend.api import config_api as cfgAPI

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
            an=request_json['an']
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}

    for entry in raw_data:
        id, tip, zi, luna, an, firma, suma, tva, total = entry

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firma", {})

        firme_zi[firma] = firme_zi.get(firma, [])
        firme_zi[firma].append(suma)

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firma": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an
        }

    return jsonify(data)

@api_routes.route('/api/cashflow/get/iesiri', methods=['POST'])
async def get_iesiri():

    request_json = await request.get_json()
    print(request_json)

    raw_data = await cAPI.get_iesiri(
            firma=request_json['firma'],
            luna=request_json['luna'],
            an=request_json['an']
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}

    for entry in raw_data:
        id, tip, zi, luna, an, firma, suma, tva, total = entry

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firma", {})

        firme_zi[firma] = firme_zi.get(firma, [])
        firme_zi[firma].append(suma)

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firma": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an
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
        id, tip, zi, luna, an, firma, suma, tva, total = entry

        data.append(
            {
                "zi": zi,
                "luna": luna,
                "an": an,
                "firma": firma,
                "suma": suma,
                "tip": tip,
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
