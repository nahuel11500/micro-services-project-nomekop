from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
from datetime import date
import os
import requests as req
import random

app = Flask(__name__)

##Local Port
PORT = 3204
HOST = '0.0.0.0'

## Others ports 
nomekop_service_url = os.getenv('NOMEKOP_SERVICE_URL', f'http://localhost:3202')

with open('{}/databases/matchs.json'.format("."), "r") as jsf:
   matchs = json.load(jsf)["matchs"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Match service!</h1>"


@app.route("/matchs", methods = ['GET'])
def get_matchs():
   res = make_response(jsonify(matchs), 200)
   return res

@app.route("/match/<player_name>/<player_request>", methods = ['GET'])
def get_match(player_name,player_request):
   return make_response(jsonify(match_already_exist(player_name,player_request)[1]), 200)

@app.route("/create_match/<player_name>/<player_request>", methods = ['POST'])
def create_match(player_name,player_request):
   """This function create a match beetween player_name and player_request. It verifies that it doesn't already exist"""
   if match_already_exist(player_name,player_request)[0]:
      return make_response(jsonify({"error": "Match already exist"}), 400)
   match = {
      "state": "created",
      "players": [player_name, player_request],
      "creation_date": date.today(),
      "winner": "NA",
      "current_round": 0,
      "score": [0, 0],
      "nomepoks": ["null", "null"]
    }
   matchs.append(match)
   return make_response(jsonify({"success": "Match created"}), 200)


# This function add a nomepok to a match.
@app.route("/add_nomekop/<player_name>/<player_request>/<nomekop>", methods = ['POST'])
def send_nomekop(player_name,player_request,nomekop):
   ## Verify if match exist
   (bool,m) = match_already_exist(player_name,player_request)
   if bool== False:
      return make_response(jsonify({"error": "Match doesn't exist"}), 400)
   ## Add pokemons to the correct part 
   if m["players"][0] == player_name:
      m["nomepoks"][0] = nomekop
   else:
      m["nomepoks"][1] = nomekop
   ## Test if both pokemons are here, if yes, start a round
   if m["nomepoks"][0] != "null" and m["nomepoks"][1] != "null":
      m["current_round"]+=1
      start_round(m["nomepoks"][0],m["nomepoks"][1])
      #Augment the round
   if erase_match(player_name,player_request): 
      matchs.append(m)   
   return make_response(jsonify({"success": "Pokemon sent"}), 200)

def match_already_exist(player_name,player_request):
   """ This function return a tuple (True,Match) or (False,"Null")"""
   for m in matchs:
      if m["players"] == [player_name,player_request] or  m["players"] == [player_request,player_name]:
         return (True,m)
   return (False,m)

def erase_match(player_name,player_request):
   for m in matchs:
      if m["players"] == [player_name,player_request] or  m["players"] == [player_request,player_name]:
         matchs.remove(m)
         return True
   return False

# Defining the types
types = ["Plant", "Water", "Air", "Fire"]

# Creating a dictionary to represent the type table
# The table will show the effectiveness of each type against the other types
# For simplicity, we use the following effectiveness scale: 0 (no effect), 0.5 (not very effective), 1 (normal), 2 (super effective)
type_table = {
    "Plant": {"Plant": 0.5, "Water": 2, "Air": 1, "Fire": 0.5},
    "Water": {"Plant": 0.5, "Water": 0.5, "Air": 1, "Fire": 2},
    "Air": {"Plant": 2, "Water": 1, "Air": 0.5, "Fire": 1},
    "Fire": {"Plant": 2, "Water": 0.5, "Air": 1, "Fire": 0.5}
}
def calculate_damage(attacker, defender):
    attacker_type = attacker["type"]
    defender_type = defender["type"]
    damage = attacker["damage"] * type_table[attacker_type][defender_type]
    return damage

def start_round(pokemon1,pokemon2):
   stat_p1 = req.get(f'{nomekop_service_url}/getNomekopsStats/{pokemon1}').json()
   stat_p2 = req.get(f'{nomekop_service_url}/getNomekopsStats/{pokemon2}').json()
   
   while stat_p1["health"] > 0 and stat_p2["health"] > 0:
        # Determine the starting Pokemon randomly
        starting_pokemon = random.choice([pokemon1, pokemon2])
        other_pokemon = pokemon2 if starting_pokemon == pokemon1 else pokemon1

        # Calculate the damage dealt by the starting Pokemon to the opponent
        damage_dealt = calculate_damage(starting_pokemon, other_pokemon)

        # Update the opponent's health
        other_pokemon["health"] -= damage_dealt

        print(f"{starting_pokemon['name']} attacks {other_pokemon['name']} for {damage_dealt} damage!")

        # Check if the opponent's health is greater than 0
        if other_pokemon["health"] > 0:
            pass
        else:
            return(f"{other_pokemon['name']} has fainted!")



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
