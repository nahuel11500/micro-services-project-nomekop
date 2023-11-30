import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3206
HOST = '0.0.0.0'


absolute_path = os.path.dirname(__file__)
relative_path = "databases/user_information.json"
full_path = os.path.join(absolute_path, relative_path)

# Fonction pour charger les informations utilisateur
def load_user_information():
    with open(full_path, "r") as jsf:
        return json.load(jsf)["user_informations"]

# Fonction pour sauvegarder les informations utilisateur
def save_user_information(user_information):
    with open(full_path, "w") as jsf:
        json.dump({"user_informations": user_information}, jsf)
# root message
#this is the welcome message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User Information service!</h1>",200)


@app.route("/creation_player",methods=['POST'])
def create_user():
    """This function get the username and the password in the body and create a new player"""
    # Charger les informations utilisateur
    user_information = load_user_information()  

    # Get data from request
    data = request.get_json()  # Assuming the data is sent in JSON format
    if data:
        username = data.get('username')
        password = data.get('password')

        # Vérifier si le nom d'utilisateur existe déjà
        for user in user_information:
            if username == user["username"]:
                return make_response("Username already exists", 400)

        # Sinon, créer le nouveau joueur
        new_player = {
            "username": username,
            "password": password,
            "role": "player"
        }
        user_information.append(new_player)
        save_user_information(user_information)  # Sauvegarder les nouvelles informations
        return make_response("Player added successfully", 200)
    else:
        return make_response("Invalid data provided", 400)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
