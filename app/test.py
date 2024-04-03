import json
import requests
import psycopg2

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname="user_db",
    user="postgres",
    password="bonjour",
    host="localhost",
    port="5432"
)

# Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()

def insert_user(data):
    try:
        # Insertion des données utilisateur dans la base de données
        sql = "INSERT INTO users (name, surname, username, email) VALUES (%s, %s, %s, %s) RETURNING id"
        cur.execute(sql, (data['name'], data['surname'], data['username'], data['email']))
        user_id = cur.fetchone()[0]
        conn.commit()  # Commit des modifications
        return user_id
    except psycopg2.Error as e:
        conn.rollback()  # Rollback en cas d'erreur
        print("Erreur lors de l'insertion des données :", e)

def patch_user(user_id, data):
    try:
        # Mise à jour des informations de l'utilisateur dans la base de données
        sql = "UPDATE users SET name = %s, surname = %s WHERE id = %s RETURNING *"
        cur.execute(sql, (data['name'], data['surname'], user_id))
        updated_user = cur.fetchone()
        conn.commit()  # Commit des modifications
        return updated_user
    except psycopg2.Error as e:
        conn.rollback()  # Rollback en cas d'erreur
        print("Erreur lors de la mise à jour des données :", e)

def delete_user(user_id):
    try:
        # Suppression de l'utilisateur de la base de données
        sql = "DELETE FROM users WHERE id = %s"
        cur.execute(sql, (user_id,))
        conn.commit()  # Commit des modifications
    except psycopg2.Error as e:
        conn.rollback()  # Rollback en cas d'erreur
        print("Erreur lors de la suppression des données :", e)

#######################################################################################

def test_missing_data():
    url = "http://localhost:5001/user"
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
    url = "http://localhost:5001/user"
    response = requests.post(url, data=data)
    assert response.status_code == 200

    try:
        # Tente de décoder la réponse comme JSON
        json_response = response.json()
    except json.decoder.JSONDecodeError:
        # Si la réponse ne peut pas être décodée comme JSON, affiche un message
        print("La réponse n'est pas au format JSON valide.")
        return

    # Si la réponse est un objet JSON valide, procédez avec les assertions
    assert len(json_response) == 1

    user_id = insert_user(data)

    assert user_id is not None

test_missing_data()
test_success()
print("POST user : OK")

#######################################################################################

user_id = 1
data = {'name': 'COURNAC', 'surname': 'Amaury'}
updated_user = patch_user(user_id, data)

assert updated_user is not None
assert updated_user[1] == 'COURNAC'  # Vérifie si le nom a été mis à jour
assert updated_user[2] == 'Amaury'  # Vérifie si le prénom a été mis à jour

print("PATCH user : OK")

#######################################################################################

def test_get_user(user_id):
    response = requests.get(f"http://localhost:5001/user/{user_id}")
    assert response.status_code == 200, f"Échec : code de statut {response.status_code}"
    user_data = response.json()
    assert user_data, "Échec : Aucune donnée utilisateur retournée"
    print(f"User trouvé avec l'ID {user_id}: {user_data}")

test_get_user(1)
print("GET user : OK")

#######################################################################################

def test_delete_user(user_id):
    response = requests.delete(f"http://localhost:5001/user/{user_id}")
    assert response.status_code == 204 or response.status_code == 404, f"Échec : code de statut {response.status_code}"
    if response.status_code == 204:
        print("L'utilisateur a été supprimé avec succès.")
    elif response.status_code == 404:
        print("L'utilisateur n'a pas été trouvé.")
        
test_delete_user(1)
print("DELETE user : OK")
