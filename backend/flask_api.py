from quart import Quart, request, jsonify, Blueprint
import asyncio

from backend.api import cashflow_api as cAPI
from backend.api import config_api as cfgAPI

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/cashflow/getIntrari', methods=['POST'])
async def get_intrari():

    request_json = await request.get_json()
    print(request_json)

    raw_data = await cAPI.get_intrari(
            firme=request_json['firme'],
            luni=request_json['luni'],
            ani=request_json['ani'],
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}

    for entry in raw_data:
        id, tip, zi, luna, an, firma, suma, tva, total = entry

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firme", {})

        firme_zi[firma] = firme_zi.get(firma, 0)
        firme_zi[firma] = firme_zi[firma] + suma

        firme_sume = data[zi].get("firme_sume", {})
        firme_sume[firma] = firme_sume.get(firma, 0) + suma

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firme": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an
        }

    return jsonify(data)

@api_routes.route('/api/cashflow/getIesiri', methods=['POST'])
async def get_iesiri():

    request_json = await request.get_json()
    print(request_json)

    raw_data = await cAPI.get_iesiri(
            firme=request_json['firme'],
            luni=request_json['luni'],
            ani=request_json['ani'],
        )

    print(raw_data)

    # Organize the data based on the "zi" index
    data = {}

    for entry in raw_data:
        id, tip, zi, luna, an, firma, suma, tva, total = entry

        if zi not in data:
            data[zi] = {}

        firme_zi = data[zi].get("firme", {})

        firme_zi[firma] = firme_zi.get(firma, 0)
        firme_zi[firma] = firme_zi[firma] + suma

        firme_sume = data[zi].get("firme_sume", {})
        firme_sume[firma] = firme_sume.get(firma, 0) + suma

        suma_zi = data[zi].get("suma", 0)
        suma_zi += suma

        data[zi] = {
            "firme": firme_zi,
            "suma": suma_zi,
            "zi": zi,
            "luna": luna,
            "an": an
        }

    return jsonify(data)

@api_routes.route('/api/cashflow/getRecents', methods=['GET'])
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
