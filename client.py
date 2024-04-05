import requests

# Remplacez l'URL par l'URL de votre point de terminaison d'API
url = 'http://localhost:8000/api/student-classrooms/'

# Remplacez le jeton d'authentification par votre propre jeton si nécessaire
headers = {'Authorization': 'Bearer your_access_token_here'}

# Envoyer une requête GET
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Afficher les données renvoyées
    print(response.json())
else:
    # Afficher un message d'erreur si la requête a échoué
    print('La requête a échoué avec le code de statut :', response.status_code)
