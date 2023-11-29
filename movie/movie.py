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
relative_path = "databases/movies.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
   movies = json.load(jsf)["movies"]



# root message
#this is the welcome message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)



if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
