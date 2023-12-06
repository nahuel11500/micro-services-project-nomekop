from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
from datetime import date

app = Flask(__name__)

##Local Port
PORT = 3204
HOST = '0.0.0.0'

with open('{}/databases/matchs.json'.format("."), "r") as jsf:
   matchs = json.load(jsf)["matchs"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Match service!</h1>"


@app.route("/matchs", methods = ['GET'])
def get_matchs():
   res = make_response(jsonify(matchs), 200)
   return res

@app.route("/create_match/<player_name>/<player_request> ", methods = ['POST'])
def create_match(player_name,player_request):
   """This function create a match beetween player_name and player_request. It verifies that it doesn't already exist"""
   if match_already_exist(player_name,player_request):
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

@app.route("/add_nomekop/<player_name>/<player_request>/<nomekop>", methods = ['POST'])
def send_nomekop(player_name,player_request,nomekop):
   if match_already_exist(player_name,player_request) == False:
      return make_response(jsonify({"error": "Match doesn't exist"}), 400)



def match_already_exist(player_name,player_request):
   for m in matchs:
      if m["players"] == [player_name,player_request] or  m["players"] == [player_request,player_name]:
         return True
   return False

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
