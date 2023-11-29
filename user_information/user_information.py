import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
absolute_path = os.path.dirname(__file__)
relative_path = "databases/user_information.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
   user_information = json.load(jsf)["user_informations"]

# root message
#this is the welcome message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User Information service!</h1>",200)


@app.route("/creation_player",methods=['GET'])
def create_user():
    """This function get the username and the password in the body and create a new player"""
    password = request.params()['password']
    username = request.params()['username']

    ## Verify that the username doesn't already exist
    ### Create the new player
    new_player = {
        "password" : password,
        "username" : username,
        "role" : "player"
    }
    user_information.append(new_player)
    return make_response("Player added successfully", 200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
