from quart import Quart, request, jsonify, render_template
from backend.flask_api import api_routes
from datetime import datetime

app = Quart(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.register_blueprint(api_routes)

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
    return await render_template('salariati.html')


if __name__ == "__main__":
    app.run(debug=True, port=5500, host='0.0.0.0')