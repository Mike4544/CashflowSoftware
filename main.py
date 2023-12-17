from quart import Quart, request, jsonify, render_template
from backend.flask_api import (
    api_routes,
    __get_angajati,
    __get_angajat,
    __get_salariu,
    __get_inventar,
    __get_flota
)
import backend.chartsAPI as chartsAPI
from backend.authAPI import auth_api
from datetime import datetime

app = Quart(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.register_blueprint(api_routes)
app.register_blueprint(auth_api)
app.register_blueprint(chartsAPI.charts_api)


@app.route('/')
@app.route('/acasa')
async def home():
    return await render_template('home.html')


@app.route('/tranzactii')
async def tranzactii():
    return await render_template(
        'tranzactii.html',
        luna=datetime.now().month,
        an=datetime.now().year
    )


@app.route('/salariati')
async def salariati():
    # If the cookies are not authed, prompt a login alert
    if not request.cookies.get('authed'):
        return """
        <script>
         let password = prompt('Parola');
           
           const response = fetch('/api/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: password
                })
            }).then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert('Parola incorecta');
                }
            });
        </script>
        """
    # Get salariati from the server
    salariati = await __get_angajati()
    return await render_template(
        'salariatiV2.html',
        angajati=salariati
    )


@app.route('/salariat/<int:id>')
async def salariat(id):
    angajat = await __get_angajat(id=id)
    print(angajat)

    # Placeholder salarii
    salarii_default = [
        {
            "luna": luna,
            "salariu": 0,
            "bonus": 0,
        } for luna in range(1, 13)
    ]

    salarii = await __get_salariu(
        an=datetime.now().year,
        angajati=[id]
    )

    if len(angajat) == 0:
        # Render a 404 page
        ...
    else:
        return await render_template(
            'salariat.html',
            an=datetime.now().year,
            nume=angajat['nume'],
            id_angajat=id,
            companie=angajat['firma'],
            salarii=salarii if len(salarii) > 0 else salarii_default
        )

@app.route('/inventar/')
async def inventar():

    angajati = await __get_angajati()

    return await render_template(
        'inventar.html',
        angajati=angajati
    )

@app.route('/inventar/<int:id>')
async def inventar_angajat(id):
    angajat = await __get_angajat(id=id)
    inventar= await __get_inventar(id)
    print(angajat)

    if len(angajat) == 0:
        # Render a 404 page
        ...
    else:
        return await render_template(
            'inventar_angajat.html',
            id_angajat=id,
            nume=angajat['nume'],
            companie=angajat['firma'],
            inventar=inventar
        )

@app.route('/flota/')
async def flota():
    masini = await __get_flota()
    return await render_template(
        'flota.html',
        vehicule=masini
    )

@app.route("/grafice/")
async def grafice():
    return await render_template(
        'charts.html',
        charts=chartsAPI.__load_charts()
    )

@app.route('/upload')
async def upload():
    integrari_default = [
        {
            "name": "S.A.G.A.",
        },
        {
            "name": "Optiunea 2",
        },
        {
            "name": "Optiunea 3",
        },
        {
            "name": "Optiunea 4",
        }
    ]

    return await render_template(
        'upload.html', integrations=integrari_default
    )


if __name__ == "__main__":
    app.run(debug=True, port=5500, host='0.0.0.0')
