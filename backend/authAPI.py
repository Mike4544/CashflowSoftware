from quart import Quart, redirect, request, jsonify, Blueprint, make_response

auth_api = Blueprint('auth_api', __name__)

DEFAULT_PASS = 'parola'

@auth_api.route('/api/auth', methods=['POST'])
async def auth():
    """
    Authenticate the user
    """
    # Get the password from the request
    rjson = await request.get_json()
    password =rjson.get('password')

    # Check if the password is correct
    if password == DEFAULT_PASS:
        # Set the auth cooke
        response = await make_response(
            jsonify({
                'status': 'success',
                'message': 'Autentificare reusita'
            })
        )
        response.set_cookie('authed', 'true', max_age=60*5)

        return response
    else:
        # Return an error
        return jsonify({
            'status': 'error',
            'message': 'Parola incorecta'
        })