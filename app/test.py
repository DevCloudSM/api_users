import json, requests

list_user = []
with open('list_user.json', 'w', encoding='utf-8') as f:
        json.dump(list_user, f, ensure_ascii=False, indent=4)
"""
if os.path.exists("list_user.json"):
    os.remove("list_user.json")
"""


def test_missing_data():        
    url= "http://localhost:5000/user"
    data = {'name': 'John', 'surname': 'Doe'}
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing data'

def test_success():
    data = {
        'name': 'cournac',
        'surname': 'amaury',
        'username': 'acournac',
        'email': 'amaury.cournac@gmail.com',
    }
    url= "http://localhost:5000/user"
    response = requests.post(url, data=data)
    assert response.status_code == 200

    json_response = json.loads(response.content.decode('utf-8'))
    assert len(json_response) == 1

    user = json_response[0]
    assert user['name'] == 'cournac'
    assert user['surname'] == 'amaury'
    assert user['username'] == 'acournac'
    assert user['email'] == 'amaury.cournac@gmail.com'

    with open('list_user.json', 'r', encoding='utf-8') as f:
        list_user = json.load(f)
    assert len(list_user) == 1

    user = list_user[0]
    assert user['name'] == 'cournac'
    assert user['surname'] == 'amaury'
    assert user['username'] == 'acournac'
    assert user['email'] == 'amaury.cournac@gmail.com'

test_missing_data()
test_success()
print("POST user : OK")


#######################################################################################

def patch_user(user_id, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.patch(f'http://localhost:5000/user/{user_id}', headers=headers, data=json.dumps(data))
    return response

user_id = 1
data = {'name': 'COURNAC', 'surname': 'Amaury'}
response = patch_user(user_id, data)

assert response.status_code == 200

user = response.json()
assert user['name'] == 'COURNAC'
assert user['surname'] == 'Amaury'


print("PATCH user : OK")



#############################################################################


url_user = "http://localhost:5000/user/"

def test_get_user(user_id):
    response = requests.get(f"{url_user}{user_id}")
    assert response.status_code == 200, f"Échec : code de statut {response.status_code}"
    user_data = response.json()
    assert user_data, "Échec : Aucune donnée utilisateur retournée"
    print(f"User trouvé avec l'ID {user_id}: {user_data}")

test_get_user(1)
print("GET user : OK")

##################################################################################

def test_delete_user(user_id):
    response = requests.delete(f"{url_user}{user_id}")
    assert response.status_code == 204 or response.status_code == 404, f"Échec : code de statut {response.status_code}"
    if response.status_code == 204:
        print("L'utilisateur a été supprimé avec succès.")
    elif response.status_code == 404:
        print("L'utilisateur n'a pas été trouvé.")
    if response.content:
        data = json.loads(response.content)
        print(data)

test_delete_user(1)
print("DELETE user : OK")
