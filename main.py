from quart import Quart, request, jsonify, render_template
from backend.flask_api import api_routes

app = Quart(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.register_blueprint(api_routes)

@app.route('/')
@app.route('/acasa')
async def home():
    return await render_template('home.html')

@app.route('/tranzactii')
async def tranzactii():
    return await render_template('tranzactii.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')