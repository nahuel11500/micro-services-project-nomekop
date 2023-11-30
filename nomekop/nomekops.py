import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

## Local port
PORT_NOMEKOP = 3202
HOST = '0.0.0.0'

## Database
absolute_path = os.path.dirname(__file__)
relative_path = "databases/nomekops.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
   nomekops = json.load(jsf)["nomekops"]

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Nomekops service!</h1>",200)

@app.route("/getNomekopStats/<nomekopName>", methods=["GET"])
def get_nomekop_stats(nomekopName):
    for nomekop in nomekops:
        if str(nomekop["name"]) == str(nomekopName):
            res = make_response(jsonify(nomekop), 200)
            return res
    return make_response(jsonify({"error": "Nomekop not found"}), 400)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT_NOMEKOP))
    app.run(host=HOST, port=PORT_NOMEKOP)
