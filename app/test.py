import json, unittest, os, requests


if os.path.exists("list_user.json"):
    os.remove("list_athlete.json")


class TestPostAthlete(unittest.TestCase):

    def test_missing_data(self):
    # Test si toutes les données nécessaires sont présentes
        
        url= "http://localhost:5000/athlete"
        data = {'name': 'John', 'surname': 'Doe'}
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Missing data')

    def test_success(self):
    # Test le cas de succès
        data = {
            'name': 'John',
            'surname': 'Doe',
            'discipline': 'Running',
            'nbmedaille': '10'
        }
        url= "http://localhost:5000/user"
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 200)

        # Access raw data using .content and decode
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(json_response), 1)

        athlete = json_response[0]
        self.assertEqual(athlete['name'], 'John')
        self.assertEqual(athlete['surname'], 'Doe')
        self.assertEqual(athlete['username'], 'johndoe')
        self.assertEqual(athlete['email'], 'john.doe@gmail.com')

        # Vérifier le fichier JSON mis à jour
        with open('list_athlete.json', 'r', encoding='utf-8') as f:
            list_athlete = json.load(f)
        self.assertEqual(len(list_athlete), 1)

        athlete = list_athlete[0]
        self.assertEqual(athlete['name'], 'John')
        self.assertEqual(athlete['surname'], 'Doe')
        self.assertEqual(athlete['username'], 'johndoe')
        self.assertEqual(athlete['email'], 'john.doe@gmail.com')

if __name__ == '__main__':
    unittest.main()

##############################------------PATCH----------#######################################

# Définition de l'URL de l'API
API_URL_athlete = 'http://localhost:5000/athlete/'

# Fonction pour envoyer une requête PATCH
def patch_athlete(athlete_id, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.patch(f'{API_URL_athlete}{athlete_id}', headers=headers, data=json.dumps(data))
    return response

# Test de modification d'un athlète existant
athlete_id = 1
data = {'name': 'Nouveau nom', 'surname': 'Nouveau prénom'}
response = patch_athlete(athlete_id, data)

# Vérification du code de statut
assert response.status_code == 200

# Vérification des données de l'athlète mis à jour
athlete = response.json()
assert athlete['name'] == 'Nouveau nom'
assert athlete['surname'] == 'Nouveau prénom'

# Test de modification d'un athlète inexistant
athlete_id = 9999
response = patch_athlete(athlete_id, data)

# Vérification du code de statut
assert response.status_code == 404

# Vérification du message d'erreur
error = response.json()
assert error['error'] == 'Athlète non trouvé'

print("Patch athlete : OK")


#####################################----------get-------------####################################

url_athlete = "http://localhost:5000/athlete/"
url_athlete_f = "http://localhost:5000/athlete/findby"

def test_get_athlete(athlete_id):
    response = requests.get(f"{url_athlete}{athlete_id}")
    if response.status_code == 200:
        print(f"Athlète trouvé avec l'ID {athlete_id}: {json.loads(response.content)}")
    else:
        print(f"Athlète introuvable avec l'ID {athlete_id}: {response.status_code}")

def test_get_athlete_findby(params):
    response = requests.get(f"{url_athlete_f}{params}")
    if response.status_code == 200:
        print(f"Athlètes trouvés avec les paramètres {params}: {json.loads(response.content)}")
    else:
        print(f"Aucun athlète trouvé avec les paramètres {params}: {response.status_code}")

# Tester get_athlete avec quelques ID
test_get_athlete(1)

# Tester get_athlete_findby avec quelques paramètres
test_get_athlete_findby({})
test_get_athlete_findby("?name=Nouveau nom")

######################################--------DELETE----------#########################################


# URL de l'API
url = "http://localhost:5000/athlete/"

# ID de l'athlète à supprimer
athlete_id = 1

# Envoi de la requête DELETE
response = requests.delete(f"{url}{athlete_id}")

# Vérification du code de retour
if response.status_code == 204:
    print("L'athlète a été supprimé avec succès.")
elif response.status_code == 404:
    print("L'athlète n'a pas été trouvé.")
else:
    print(f"Une erreur est survenue : {response.status_code}")

# Affichage du contenu de la réponse
if response.content:
    data = json.loads(response.content)
    print(data)


