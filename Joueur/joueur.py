from flask import Flask, request, jsonify, make_response
import requests
import json
import os

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/Joueur.json'.format("."), "r") as jsf:
   players = json.load(jsf)["joueurs"]

# Définissez l'URL du service Booking en utilisant une variable d'environnement
times_service_url = os.getenv('TIMES_SERVICE_URL', 'http://127.0.0.1:3202')

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"




@app.route("/players", methods=['GET'])
def get_players():
   res = make_response(jsonify(players), 200)
   return res


## Return the list of players
@app.route("/player/<player_name>", methods=['GET'])
def get_player(player_name):
   for player in players:
      if player["username"] == player_name:
         return make_response(jsonify(player), 200)
   return(make_response("Player not found", 400))

## Create a match beetween the player doing the request and the player doind the request (in the body)
@app.route("/player/create_match/<player_name>/<player_request>", methods=['POST'])
def create_match(player_name,player_request):

   for player in players:
      if player["username"] == player_name:
         ## Create a match with the player if he exist
         return (make_response("Not yet Implemetend", 400))  
   return(make_response("Player not found", 400))   



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
