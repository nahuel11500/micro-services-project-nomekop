import requests

# URL of the Flask APP
base_url = 'http://localhost:3200'

# Data Credentials
login_data = {
    'username': 'Nahuel',
    'password': 'Nahuel'
}

# Create a session to maintain cookies
session = requests.Session()

# For connection
login_response = session.post(f'{base_url}/login', json=login_data)

# Check if the connection is successful
if login_response.ok:
    # Extract the JSON 
    response_data = login_response.json()
    print("Connecté avec succès.")
    print("Contenu de la page de connexion:", response_data)

    # Extract the session id 
    session_id = response_data.get('Session_Id')
    session.cookies.set('session_id', session_id)

    ## Access a protected route
    protected_response = session.get(f'{base_url}/player/get_info_other_player')

    print("Statut de la requête à la route protégée:", protected_response.status_code)
    print("Contenu de la route protégée:", protected_response.text)
else:
    print("Échec de la connexion.")
    print("Raison:", login_response.text)