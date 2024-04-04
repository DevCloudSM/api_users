import json, os, requests
import psycopg2
from psycopg2 import sql
from flask import Flask, request, jsonify, Response, render_template

from requests.structures import CaseInsensitiveDict
app = Flask(__name__) 

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname="user_db",
    user="postgres",
    password="bonjour",
    host="postgres_database",
    port="5432"
)
cursor = conn.cursor()
navbar_html = [ {"id":"1", "name":"Home", "url":"/"}, 
                {"id":"2", "name":"Add a user", "url":"/user/add"},
                {"id":"3", "name":"Modify a user", "url":"/user/modify"},
                {"id":"4", "name":"Find a user", "url":"/user/findby/search"},
                {"id":"5", "name":"Delete a user", "url":"/user/delete"}, 
                {"id":"6", "name":"Show all users", "url":"/user"}]


@app.route("/") 
def accueil(): 
    # Ouvre le fichier index.html lors de la connection à l'api
    return render_template("index.html", navbar=navbar_html)

@app.route('/user/add', methods = ['GET'])
def affichage_user():
    # Ouvre la page html qui permet à l'utilisateur de remplir le formulaire de création d'utilisateur
    return render_template("add_user.html", navbar=navbar_html)

@app.route('/user/add',methods = ['POST']) 
def post_user():
    content_type = request.headers['Content-Type']

    # Traitement des formulaires HTML
    if content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
        surname = request.form.get('surname')
        username = request.form.get('username')
        email = request.form.get('email')


    # Traitement des requêtes JSON
    elif content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        username = data.get('username')
        email = data.get('email')

    # Vérifie que toutes les données nécessaires sont présentes
    if not name or not surname or not username or not email:
        return jsonify({"error": "Missing data"}), 400

    # Insérer les données dans la base de données
    try:
        cursor.execute(
            """
            INSERT INTO users (name, surname, username, email) VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (name, surname, username, email)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        user_data = {
            'id': user_id,
            'name': name,
            'surname': surname,
            'username': username,
            'email': email
        }
        if content_type == 'application/json':
            return jsonify(user_data), 201
        else:   
            return render_template('add_user_result.html', user=user_data, navbar=navbar_html)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    

@app.route('/user/<int:userId>', methods = ['GET'])
def get_user(userId):
    # Récupérer l'utilisateur à partir de la base de données
    try:
        cursor.execute(
            """
            SELECT * FROM users WHERE id = %s LIMIT 1000;
            """,
            (userId,)
        )
        user = cursor.fetchone()
        if user:
            user_data = {
                'id': user[0],
                'name': user[1],
                'surname': user[2],
                'username': user[3],
                'email': user[4]
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/findby/search') 
def find_user_by_interface():
    return render_template('findby_search.html', navbar=navbar_html)

@app.route('/user/findby/result', methods = ['POST']) 
def find_user_by_interface_result():
    if request.method == 'POST':
        data = request.form['data']
        attribut = request.form['attribut']
        url = 'http://localhost:5000/user/findby'
        if attribut == 'name':
            params = {'name': data}
        elif attribut == 'surname':
            params = {'surname': data}
        elif attribut == 'username':
            params = {'username': data}
        elif attribut == 'email':
            params = {'email': data}
        else :
            return jsonify({"error": "No user found matching the search criteria"}), 404
        
        found_user = requests.get(url, params=params)
        
        if found_user.status_code == 200:
            found_users = found_user.json()
            if found_users:
                return render_template('findby_result.html', users=found_users, navbar=navbar_html)
            else:
                return jsonify({"error": "No user found matching the search criteria"}), 404
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
    elif request.method == 'GET':
        return "<p>coucou</p>\n"
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

@app.route('/user/findby',methods = ['GET']) 
def get_user_findby():
    # Récupérer les paramètres de requête
    user_id = request.args.get('id')
    name = request.args.get('name')
    surname = request.args.get('surname')
    username = request.args.get('username')
    email = request.args.get('email')

    # Initialiser une liste pour stocker les utilisateurs correspondant aux critères de recherche
    matched_user = []

    # Construire la requête SQL en fonction des critères de recherche fournis
    query = sql.SQL("SELECT * FROM users WHERE true")
    params = []
    if user_id:
        query += sql.SQL(" AND id = %s")
        params.append(user_id)
    if name:
        query += sql.SQL(" AND LOWER(name) = LOWER(%s)")
        params.append(name)
    if surname:
        query += sql.SQL(" AND LOWER(surname) = LOWER(%s)")
        params.append(surname)
    if username:
        query += sql.SQL(" AND LOWER(username) = LOWER(%s)")
        params.append(username)
    if email:
        query += sql.SQL(" AND LOWER(email) = LOWER(%s)")
        params.append(email)
    try:
        print(query)
        print(params)
        cursor.execute(query, params)
        users = cursor.fetchall()
        if users:
            for user in users:
                user_data = {
                    'id': user[0],
                    'name': user[1],
                    'surname': user[2],
                    'username': user[3],
                    'email': user[4]
                }
                matched_user.append(user_data)
            return jsonify(matched_user), 200
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
    except Exception as e:
        print(e) 
        return jsonify({"error": str(e)}), 500


@app.route('/user/modify')
def affichage_recherche_modify():
    return render_template("modification_search.html", navbar=navbar_html)

@app.route('/user/modify/suite', methods =['POST'])
def recovery_of_user_to_modify():
    if request.method == 'POST':
        data = request.form['data']
        attribut = request.form['attribut']
        url = 'http://localhost:5000/user/findby'
        if attribut == 'name':
            params = {'name': data}
        elif attribut == 'surname':
            params = {'surname': data}
        elif attribut == 'username':
            params = {'username': data}
        elif attribut == 'email':
            params = {'email': data}
        else :
            return jsonify({"error": "No user found matching the search criteria"}), 404
        
        found_user = requests.get(url, params=params)
        
        if found_user.status_code == 200:
            found_users = found_user.json()
            if found_users:
                # Supposons que vous voulez modifier le premier utilisateur trouvé
                first_user = found_users[0]
                user_id = first_user.get('id')
                name = first_user.get('name')
                surname = first_user.get('surname')
                username = first_user.get('username')
                email = first_user.get('email')
                return render_template('modification_form.html', found_user_id = user_id, found_user_name=name, found_user_surname=surname, found_user_username=username, found_user_email=email, navbar=navbar_html)
            else:
                return jsonify({"error": "No user found matching the search criteria"}), 404
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
    elif request.method == 'GET':
        return "<p>coucou</p>\n"
    else:
        return jsonify({"error": "Method Not Allowed"}), 405
        
@app.route('/user/<int:userId>', methods = ['PATCH'])
def modification_user(userId): 
     # Recherche de l'utilisateur à modifier
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Récupération des données JSON de la requête
    data = {}
    if request.is_json:
        data = request.get_json()

    # Mise à jour des informations de l'utilisateur
    for key, value in data.items():
        cursor.execute(f"UPDATE users SET {key} = %s WHERE id = %s", (value, userId))

    # Enregistrement des modifications
    conn.commit()

    # Récupération des informations de l'utilisateur mis à jour
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
    user = cursor.fetchone()

    return jsonify(user), 200

@app.route('/user/modify/result', methods = ['POST'])
def affichage_donnée_modifier():
    content_type = request.headers['Content-Type']
    if content_type == 'application/x-www-form-urlencoded':
        user_id = request.form.get('id')
        name = request.form.get('name')
        surname = request.form.get('surname')
        username = request.form.get('username')
        email = request.form.get('email')
    data_user = {'name': name, 'surname': surname, 'username':username, 'email': email}
    headers = {'Content-Type': 'application/json'}
    data=json.dumps(data_user)
    response = requests.patch(f'http://localhost:5000/user/{user_id}', headers=headers, data=data)
    if response.status_code == 200:
        return render_template("modification_result.html", navbar = navbar_html)
    else:
        return 'La modification des données a échoué', response.status_code
    
@app.route('/user/delete')
def suppression_user_interface():
    return render_template('delete_search.html', navbar=navbar_html)

@app.route('/user/delete/suite', methods =['POST'])
def recovery_of_user_to_delete():
    if request.method == 'POST':
        data = request.form['data']
        attribut = request.form['attribut']
        url = 'http://localhost:5000/user/findby'
        if attribut == 'name':
            params = {'name': data}
        elif attribut == 'surname':
            params = {'surname': data}
        elif attribut == 'username':
            params = {'username': data}
        elif attribut == 'email':
            params = {'email': data}
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
        
        found_user = requests.get(url, params=params)
        
        if found_user.status_code == 200:
            found_users = found_user.json()
            if found_users:
                # Utilisation de render_template_string pour générer le tableau HTML
                return render_template('delete_table.html', users=found_users, navbar=navbar_html)
            else:
                return jsonify({"error": "No user found matching the search criteria"}), 404
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
    elif request.method == 'GET':
        return "<p>coucou</p>\n"
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

@app.route('/user/delete/result', methods = ['POST'])
def affichage_donnée_delete():
    content_type = request.headers['Content-Type']
    if content_type == 'application/x-www-form-urlencoded':
        user_id = request.form.get('id')
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f'http://localhost:5000/user/{user_id}', headers=headers)
    if response.status_code == 204:
        return render_template("delete_result.html", navbar=navbar_html)
    else:
        return 'La suppression des données a échoué', response.status_code

@app.route('/user/<int:userId>', methods = ['DELETE'])
def suppression_user(userId): 
    try:
        # Supprimer l'utilisateur de la base de données
        cursor.execute(
            """
            DELETE FROM users WHERE id = %s;
            """,
            (userId,)
        )
        conn.commit()
        return jsonify({}), 204
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/user', methods=['GET'])
def affichage():
    content_type = request.headers['Content-Type']

    # Traitement des formulaires HTML
    if content_type == 'application/x-www-form-urlencoded':
        try:
            # Exécuter une requête pour sélectionner toutes les lignes de la table users
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            if users:
                # Convertir les résultats en une liste de dictionnaires
                users_data = []
                for user in users:
                    user_data = {
                        'id': user[0],
                        'name': user[1],
                        'surname': user[2],
                        'username': user[3],
                        'email': user[4]
                    }
                    users_data.append(user_data)
                return render_template('findby_result.html', navbar=navbar_html, users=users_data)
            else:
                return jsonify({"error": "No users found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    if content_type == 'application/json':
        try:
            # Exécuter une requête pour sélectionner toutes les lignes de la table users
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            if users:
                # Convertir les résultats en une liste de dictionnaires
                users_data = []
                for user in users:
                    user_data = {
                        'id': user[0],
                        'name': user[1],
                        'surname': user[2],
                        'username': user[3],
                        'email': user[4]
                    }
                    users_data.append(user_data)
                return jsonify(users_data)
            else:
                return jsonify({"error": "No users found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
if __name__ == "__main__": 
    app.run(host='0.0.0.0', port='5000', debug=True)
