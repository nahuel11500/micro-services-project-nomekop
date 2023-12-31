from flask import Flask, request, jsonify, make_response
import json
import os
import requests
app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

absolute_path = os.path.dirname(__file__)
relative_path = "databases/stats.json"
full_path = os.path.join(absolute_path, relative_path)
with open(full_path, "r") as jsf:
    users = json.load(jsf)["stats"]

#Définie l'URL du service Booking en utilisant une variable d'environnement
# (la seconde valeur est la valeur par défaut)
booking_service_url = os.getenv('BOOKING_SERVICE_URL', 'http://127.0.0.1:3201')


#Définie l'URL du service Moovie en utilisant une variable d'environnement
movie_service_url = os.getenv('MOVIE_SERVICE_URL', 'http://127.0.0.1:3200')


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Stat service!</h1>"



if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    # Start the Flask app on the specified host and port in debug mode.
    app.run(host=HOST, port=PORT, debug=True)
