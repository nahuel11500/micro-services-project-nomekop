from flask import Flask, request, jsonify, make_response
import json
import os
import requests
import uuid
app = Flask(__name__)

### Local Port
PORT = 3200
HOST = '0.0.0.0'

## Others ports
PORT_USER_INFORMATION = 3206
PORT_PLAYER= 3201
PORT_MATCH=3204
PORT_STAT=3205
PORT_STORE=3203
PORT_NOMEKOPS=3202

absolute_path = os.path.dirname(__file__)
relative_path = "databases/session.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
    sessions = json.load(jsf)["session"]

## Define services url using either env variables if the app is started with docker or localhost.
user_information_service_url = os.getenv('USER_INFORMATION_SERVICE_URL', f'http://localhost:{PORT_USER_INFORMATION}')
player_service_url = os.getenv('PLAYER_SERVICE_URL', f'http://localhost:{PORT_PLAYER}')
match_service_url = os.getenv('MATCH_SERVICE_URL', f'http://localhost:{PORT_MATCH}')
stat_service_url = os.getenv('STAT_SERVICE_URL', f'http://localhost:{PORT_STAT}')
store_service_url = os.getenv('STORE_SERVICE_URL', f'http://localhost:{PORT_STORE}')
nomekop_service_url = os.getenv('NOMEKOP_SERVICE_URL', f'http://localhost:{PORT_NOMEKOPS}')



@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

##########################################   Everyone     ########################################## 

@app.route("/login", methods=['POST'])
def login():
    """This function get the username and the password in the body, verifies if it's okay and then return a session id"""
    data = request.get_json()  # Assuming the data is sent in JSON format
    if data:
        req = requests.get(f'{user_information_service_url}/credentials_verification', json=data)
        ### Login unsuccessful
        if req.status_code == 400:
            response = make_response(jsonify(req.json()))
            response.status_code = 400
            return response
        ### Login succesful
        elif req.status_code == 200:
            data = req.json() 
            session_id= str(uuid.uuid4())  # Generate a unique UUID
            session = {
                "session_id": session_id,
                "name":data.get('username'), 
                "role":data.get('role')
            }
            sessions.append(session)
            return make_response(jsonify({"message": "Login successful", "Session_Id": session_id}), 200) 
    else:
        return make_response("Invalid data provided", 400)


@app.route("/create_account", methods=['POST'])
def create_account():
    """This function get the username and the password in the body and create an account"""
    data = request.get_json()  # Assuming the data is sent in JSON format
    if data:
        req = requests.post(f'{user_information_service_url}/creation_player', json=data)
        response = make_response(jsonify(req.json()))
        response.status_code = 200
        return response
    else:
        return make_response("Invalid data provided", 400)

######################################### Authentification 

# Function that check the session id
def is_logged_in(session_id):
    # check if the session id is in th list
    for session in sessions:
        if session["session_id"] == session_id:
            return True
    return False

# A decorator use to protect routes that needs authentification
def login_required(f):
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')  # extract the session_id from cookie
        if not session_id or not is_logged_in(session_id):
            return make_response("Incorrect login", 400)
        return f(*args, **kwargs)
    return decorated_function

##########################################   Player     ########################################## 

## 2)b)i)
# Route protected by authentification
@app.route('/player/get_info_other_player', endpoint='get_infos_players')
@login_required
def get_infos_players ():
    try:
        req = requests.get(f'{player_service_url}/players')
        # Check if the request was successful (status code 200)
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(remove_fields(req.json(),["credit","nomekops"])))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": "Failed to retrieve players info"}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)

@app.route('/player/buyNomekop/<nomekop>', endpoint='buy_nomekop', methods=['PUT'])
@login_required
def buy_nomekop (nomekop):
    try:
        player = request.cookies.get('session_id')
        req = requests.put(f'{player_service_url}/buy/{get_name(player)}/{nomekop}')
        # Check if the request was successful (status code 200)
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": "Failed to retrieve buying info"}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)



@app.route('/player/get_nomekops', endpoint='get_player_nomekops', methods=['GET'])    
@login_required
def get_player_nomekops():
    """This function return the list of pokemons associated with a player"""
    requester = get_name(request.cookies.get('session_id'))
    try:
        req = requests.get(f"{player_service_url}/player/get_nomekops/{requester}")
        # Check if the request was successful (status code 200)
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": req.text}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)


#################################################################################################
##########################################   Store     ########################################## 
#################################################################################################

@app.route('/store/getNomekopsPrices', endpoint='get_nomekops_prices')
@login_required
def get_nomekops_prices():
    try:
        req = requests.get(f'{store_service_url}/getNomekopsPrices')
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": "Failed to retrieve store info"}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)

##########################################   Nomekops     ##########################################

@app.route('/nomekops/nomekopstats/<nomekopName>', endpoint='get_nomekops_stats')
@login_required
def get_nomekops_stats(nomekopName):
    try:
        req = requests.get(f'{nomekop_service_url}/getNomekopStats/{nomekopName}')
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": "Failed to retrieve nomekop info"}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)

##########################################   User Informations      ########################################## 

##########################################   Match      ########################################## 

### This function create a match beetween the player and the requested.
@app.route('/player/match/<player_name>', endpoint='create_match', methods=['POST'])    
@login_required
def create_match(player_name):
    requester = get_name(request.cookies.get('session_id'))
    ###Test if the player_name exist
    try:
        req = requests.get(f"{player_service_url}/player/{player_name}")
        if req.status_code == 200:
           pass
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": req.text}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)
    
    try:
        req = requests.post(f"{match_service_url}/create_match/{requester}/{player_name}")
        # Check if the request was successful (status code 200)
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": req.text}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)

##########################################   Stat       ########################################## 


#########################################    Else       ########################################## 
def get_role(session_id):
    """This function return the role of someone based on its session id"""
    for session in sessions:
        if session_id == session["session_id"]:
            return session["role"]

def get_name(session_id):
    """This function return the role of someone based on its session id"""
    print(sessions)
    for session in sessions:
        if str(session_id) == session["session_id"]:
            return session["name"]
      
def remove_fields(json,fields):
    for item in json:
        for field in fields:
            if field in item:
                del item[field]
    return json


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    # Start the Flask app on the specified host and port in debug mode.
    app.run(host=HOST, port=PORT, debug=True)
