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

absolute_path = os.path.dirname(__file__)
relative_path = "databases/session.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
    sessions = json.load(jsf)["session"]
print(sessions)
#Définie l'URL du service Booking en utilisant une variable d'environnement
# (la seconde valeur est la valeur par défaut)
booking_service_url = os.getenv('BOOKING_SERVICE_URL', 'http://127.0.0.1:3201')


#Définie l'URL du service Moovie en utilisant une variable d'environnement
movie_service_url = os.getenv('MOVIE_SERVICE_URL', 'http://127.0.0.1:3200')

#URL de secours si la variable d'environnement n'est pas définie
if not booking_service_url:
    movie_service_url = 'http://127.0.0.1:3201'


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

##########################################   Everyone     ########################################## 

@app.route("/login", methods=['POST'])
def login():
    """This function get the username and the password in the body, verifies if it's okay and then return a session id"""
    data = request.get_json()  # Assuming the data is sent in JSON format
    if data:
        req = requests.get(f'http://localhost:{PORT_USER_INFORMATION}/credentials_verification', json=data)
        ### Login unsuccessful
        if req.status_code == 400:
            return (req)
        ### Login succesful
        elif req.status_code == 200:
            data = req.json() 
            session_id= str(uuid.uuid4())  # Generate a unique UUID
            session = {
                "session_id": session_id,
                "username":data.get('username'), 
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
        req = requests.post(f'http://localhost:{PORT_USER_INFORMATION}/creation_player', json=data)
        return(req)
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
@app.route('/player/get_info_other_player')
@login_required
def get_infos_players ():
    try:
        req = requests.get(f'http://localhost:{PORT_PLAYER}/players')
        # Check if the request was successful (status code 200)
        if req.status_code == 200:
            # Create a response with the JSON content
            response = make_response(jsonify(req.json()))
            response.status_code = 200
            return response
        else:
            # Handle the error, for example, return an error response
            return make_response(jsonify({"error": "Failed to retrieve players info"}), req.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return make_response(jsonify({"error": f"Request error: {str(e)}"}), 500)

##########################################   Store     ########################################## 

##########################################   User Informations      ########################################## 

##########################################   Match      ########################################## 

##########################################   Stat       ########################################## 


#########################################    Else       ########################################## 
def get_role(session_id):
    """This function return the role of someone based on its session id"""
    for session in sessions:
        if session_id == session["session_id"]:
            return session["role"]

def get_name(session_id):
    """This function return the role of someone based on its session id"""
    for session in sessions:
        if session_id == session["session_id"]:
            return session["name"]

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    # Start the Flask app on the specified host and port in debug mode.
    app.run(host=HOST, port=PORT, debug=True)
