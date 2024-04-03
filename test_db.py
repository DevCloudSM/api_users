import os
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname="user_db",
    user="postgres",
    password="bonjour",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

navbar_html = [{"id": "1", "name": "Home", "url": "/"},
               {"id": "2", "name": "Add a user", "url": "/user"},
               {"id": "3", "name": "Modify a user", "url": "/user/modify"},
               {"id": "4", "name": "Find a user", "url": "/user/findby/search"},
               {"id": "5", "name": "Delete a user", "url": "/user/delete"},
               {"id": "6", "name": "Show all users", "url": "/affichage"}]


@app.route("/")
def accueil():
    # Ouvre le fichier index.html lors de la connection à l'api
    return render_template("index.html", navbar=navbar_html)


@app.route('/user')
def affichage_user():
    # Ouvre la page html qui permet à l'utilisateur de remplir le formulaire de création d'utilisateur
    return render_template("add_user.html", navbar=navbar_html)


@app.route('/user', methods=['POST'])
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
        return jsonify(user_data), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/user/<int:userId>', methods=['GET'])
def get_user(userId):
    # Récupérer l'utilisateur à partir de la base de données
    try:
        cursor.execute(
            """
            SELECT * FROM users WHERE id = %s;
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


@app.route('/user/findby', methods=['GET'])
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
    query = sql.SQL("""
        SELECT * FROM users WHERE (true)
    """)
    if user_id:
        query += sql.SQL(" AND id = %s")
    if name:
        query += sql.SQL(" AND name = %s")
    if surname:
        query += sql.SQL(" AND surname = %s")
    if username:
        query += sql.SQL(" AND username = %s")
    if email:
        query += sql.SQL(" AND email = %s")

    # Exécuter la requête SQL avec les valeurs des paramètres
    try:
        cursor.execute(query, (user_id, name, surname, username, email))
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
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', debug=True)