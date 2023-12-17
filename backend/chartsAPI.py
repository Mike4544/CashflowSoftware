import json
from quart import Quart, request, jsonify, Blueprint
import os

charts_api = Blueprint('charts_api', __name__)

def __load_charts():
    """
    Load the charts from the __charts_cache folder
    """
    charts = []

    # Get the charts from the cache folder
    files = os.listdir('__charts_cache')

    # Return the charts
    for file in files:
        with open(f'__charts_cache/{file}') as f:
            charts.append(json.load(f))

    return charts

@charts_api.route('/api/charts/add', methods=['POST'])
async def save_chart():
    """
    Save a chart + overwrite
    """
    # Get the chart from the request
    chart = await request.get_json()

    # Check if the folder exists
    if not os.path.exists('__charts_cache'):
        os.mkdir('__charts_cache')

    # Save the chart
    with open(f'__charts_cache/{chart["id"]}.json', 'w') as f:
        json.dump(chart, f)

    # Return a success message
    return jsonify({
        'status': 'success',
        'message': 'Chart saved'
    })

@charts_api.route('/api/charts/delete', methods=['POST'])
async def delete_chart():
    """
    Delete a chart
    """
    # Get the chart from the request
    chart = await request.get_json()

    # Delete the chart
    os.remove(f'__charts_cache/{chart["id"]}.json')

    # Return a success message
    return jsonify({
        'status': 'success',
        'message': 'Chart deleted'
    })