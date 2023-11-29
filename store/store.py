import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT_STORE = 3203
PORT_NOMEKOP = 3202
HOST = '0.0.0.0'
absolute_path = os.path.dirname(__file__)
relative_path = "databases/store.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
    items = json.load(jsf)["store"]

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the store service!</h1>",200)

@app.route("/getNomekopsPrices", methods=["GET"])
def get_nomekops_prices():
    res = make_response(jsonify(nomekop), 200)

@app.route("/getNomekopStats/<nomekopName>", methods=["GET"])
def get_nomekop_stats(nomekopName):
    req = requests.get(f'http://localhost:{PORT_NOMEKOP}/getNomekopStats/{nomekopName}')
    return make_response(req.json(), 200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT_STORE))
    app.run(host=HOST, port=PORT_STORE)