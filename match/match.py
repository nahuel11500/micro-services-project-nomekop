from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

##Local Port
PORT = 3204
HOST = '0.0.0.0'

with open('{}/databases/matchs.json'.format("."), "r") as jsf:
   matchs = json.load(jsf)["matchs"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Match service!</h1>"

# This route handles a GET request to '/showtimes'.
@app.route("/matchs", methods = ['GET'])
def get_matchs():
   res = make_response(jsonify(matchs), 200)
   return res

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
