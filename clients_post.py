import requests

# URL de votre point de terminaison d'authentification
login_url = 'http://localhost:8000/api/login/'

# Informations d'identification pour l'authentification
username = 'kbjean.elie'
password = 'qwerty'

# Données à envoyer avec la requête POST
data = {'username': username, 'password': password}

# Envoyer une requête POST pour obtenir un jeton d'authentification
response = requests.post(login_url, data=data)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Extraire le jeton d'authentification à partir de la réponse
    token = response.json()['access']
    
    # URL de votre point de terminaison d'API
    api_url = 'http://localhost:8000/api/students/1/subjects/'

    # Inclure le jeton d'authentification dans l'en-tête de la requête
    headers = {'Authorization': f'Bearer {token}'}

    # Envoyer une requête GET à votre point de terminaison d'API avec le jeton d'authentification
    response = requests.get(api_url, headers=headers)

    # Vérifier si la requête a réussi (code de statut HTTP 200)
    if response.status_code == 200:
        # Afficher les données renvoyées
        print(response.json())
    else:
        # Afficher un message d'erreur si la requête a échoué
        print('La requête a échoué avec le code de statut :', response.status_code)
else:
    # Afficher un message d'erreur si la requête POST pour l'authentification a échoué
    print('La requête POST pour l\'authentification a échoué avec le code de statut :', response.status_code)
