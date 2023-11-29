from flask import Flask, request, jsonify, make_response
import requests
import json
import os

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

# Définissez l'URL du service Booking en utilisant une variable d'environnement
times_service_url = os.getenv('TIMES_SERVICE_URL', 'http://127.0.0.1:3202')
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
