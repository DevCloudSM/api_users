import json, os
from flask import Flask, request, jsonify, Response, render_template
import requests 
from requests.structures import CaseInsensitiveDict
app = Flask(__name__) 

@app.route("/") 
def accueil(): 
    # Ouvre le fichier index.html lors de la connection à l'api
    return index_html 

@app.route('/user')
def affichage_user():
    # Ouvre la page html qui permet à l'utilisateur de remplir le formulaire de création d'utilisateur
    return user_test_html

@app.route('/user',methods = ['POST']) 
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

    # Vérifie que le type de contenu est 'application/x-www-form-urlencoded'
    if request.headers['Content-Type'] != 'application/x-www-form-urlencoded':
        return jsonify({"error": "Expected form-urlencoded data"}), 415

    # Récupére les données du formulaire HTML
    name = request.form.get('name')
    surname = request.form.get('surname')
    username = request.form.get('username')
    email = request.form.get('email')

    # Vérifie que toutes les données nécessaires sont présentes
    if not name or not surname or not username or not email:
        return jsonify({"error": "Missing data"}), 400

    # Vérifie si le fichier JSON existe et s'il n'est pas vide
    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        # Ouvre le fichier JSON existant pour la lecture
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)
    else:
        # Si le fichier n'existe pas ou est vide, initialise list_user à une liste vide
        list_user = []

    # Génére un ID unique pour le nouvel user
    user_id = 1
    if list_user:
        # S'il y a des user déjà présents, incrémente l'ID en fonction du nombre d'utilisateur
        user_id = max(user['id'] for user in list_user) + 1

    # Crée un dictionnaire Python avec les données récupérées et l'ID généré
    user_data = {
        'id': user_id,
        'name': name,
        'surname': surname,
        'username': username,
        'email': email
    }

    # Ajoute les nouvelles données à la liste python
    list_user.append(user_data)

    # Réécri le fichier JSON avec la liste mise à jour
    with open('list_user.json', 'w', encoding='utf-8') as f:
        json.dump(list_user, f, ensure_ascii=False, indent=4)

    # Converti la liste d'athlètes en JSON
    json_response = json.dumps(list_user, ensure_ascii=False, indent=4)
    
    # Retourne la réponse JSON
    return Response(json_response, content_type='application/json'), 200

@app.route('/user/<int:userId>', methods = ['GET'])
def get_user(userId):
    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)
    else:
        return jsonify({"error": "User not found"}), 404

    # Recherche l'athlète avec l'ID
    for user in list_user:
        if user['id'] == userId:
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404

@app.route('/user/findby',methods = ['GET']) 
def get_user_findby():
    # Récupére les paramètres de requête
    user_id = request.args.get('id')
    name = request.args.get('name')
    surname = request.args.get('surname')
    username = request.args.get('username')
    email = request.args.get('email')

    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)
    else:
        return jsonify({"error": "No user found"}), 404

    # Initialise une liste pour stocker les athlètes correspondant aux critères de recherche
    matched_user = []

    # Parcourir tous les athlètes pour les filtrer en fonction des critères de recherche
    for user in list_user:
        if (user_id is None or str(user['id']) == user_id) and \
           (username is None or user['username'] == username) and \
           (name is None or user['name'] == name) and \
           (surname is None or user['surname'] == surname) and \
           (email is None or str(user['email']) == email):
            matched_user.append(user)

    # Vérifie s'il y a des athlètes correspondant aux critères de recherche
    if matched_user:
        return jsonify(matched_user), 200
    else:
        return jsonify({"error": "No user found matching the search criteria"}), 404

@app.route('/user/modify')
def affichage_recherche_modify():
    return modification_html

# Permet d'utiliser la fonction findby avec un formulaire

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
                name = first_user.get('name')
                surname = first_user.get('surname')
                username = first_user.get('username')
                email = first_user.get('email')
                return render_template('modification_form.html', found_user_name=name, found_user_surname=surname, found_user_username=username, found_user_email=email)
            else:
                return jsonify({"error": "No user found matching the search criteria"}), 404
        else:
            return jsonify({"error": "No user found matching the search criteria"}), 404
    elif request.method == 'GET':
        return "<p>coucou</p>\n"
    else:
        return jsonify({"error": "Method Not Allowed"}), 405
        

@app.route('/user/modify/<int:userID>', methods = ['PUT'])
def update_user(user_Id):
###################################################################  A modifié  ######################
    new_user_data = get_user_findby(user_Id)
    
    # Charge la liste de users
    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)
    else:
        return jsonify({"error": "No user found"}), 404
    
    
    if request.method == 'PUT':
        # Récupérer les données du formulaire
        user['name'] = request.form['name']
        user['surname'] = request.form['surname']
        user['username'] = request.form['username']
        user['email'] = request.form['email']
        
    # Rechercher l'utilisateur dans votre stockage de données
    user_to_update = None
    for user in list_user:
        if user['id'] == user_Id:
            user_to_update = user
            break
    
    # Si l'utilisateur est trouvé, mettre à jour ses informations
    if user_to_update:
        # Mettre à jour les informations de l'utilisateur avec les nouvelles données
        user_to_update.update(new_user_data)
        
        # Sauvegarder les modifications dans votre stockage de données (par exemple, un fichier JSON)
        # Réécri le fichier JSON avec la liste mise à jour
        with open('list_user.json', 'w', encoding='utf-8') as f:
            json.dump(list_user, f, ensure_ascii=False, indent=4)

        # Converti la liste d'athlètes en JSON#################
        save_users_to_file = json.dumps(list_user, ensure_ascii=False, indent=4)
       
        
        # Renvoyer une réponse indiquant que les informations de l'utilisateur ont été mises à jour avec succès
        return jsonify({"message": "User information updated successfully"}), 200
    else:
        # Renvoyer une réponse indiquant que l'utilisateur n'a pas été trouvé
        return jsonify({"error": "User not found"}), 404
###################################################################  A modifié  ######################


@app.route('/test', methods=['GET'])
def test():
    # Ouvrir le fichier JSON pour lecture
    with open('list_user.json', 'r', encoding='utf-8') as f:
        try:
            # Charger le contenu JSON
            data = json.load(f)
            return jsonify(data), 200
        except json.JSONDecodeError as e:
            # Gérer les erreurs de décodage JSON
            return jsonify({"error": str(e)}), 500

# Page d'accueil
index_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>API_user</title>
</head>
<body>
    <h1>User Management</h1>
    <h2>Please select one option</h2>
    <ul>
        <li><a href="/user">Add a user</a></li>
        <li><a href="/user/modify">Modify a user</a></li>
        <li><a href="/user">Find a user</a></li>
    </ul>
</body>
</html>"""

# page pour la route /user 'PUT'
user_test_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>API user</title>
</head>
    <body>
        <h1>User management</h1>
        <h2>Add a user : </h2>
            <form action="/user" method="POST" enctype="application/json">
                <label for="disease">Name : </label>
                <input type="text" name="name" id="name">
                <br>
                <label for="disease">Surname : </label>
                <input type="text" name="surname" id="surname">
                <br>
                <label for="disease">username : </label>
                <input type="text" name="username" id="username">
                <br>
                <label for="disease">email : </label>
                <input type="text" name="email" id="email">
                <br>
                <input type="submit" value="Add">
            </form>
    </body>
</html>"""

# page pour la route /user/modify
modification_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Search for a user to edit it</title>
</head>
<body>
    <h1>Search for a user to edit it</h1>
    <h3>Please select a type of data to research</h3>
    <form action=/user/modify/suite method="POST">
        <input type="radio" id="name" name="attribut" value="name">
        <label for="name">Name</label>
        <input type="radio" id="surname" name="attribut" value="surname">
        <label for="surname">Surname</label>
        <input type="radio" id="username" name="attribut" value="username">
        <label for="username">Username</label>
        <input type="radio" id="email" name="attribut" value="email">
        <label for="email">Email</label><br><br>
        <label for="data">Data :</label>
        <input type="text" id="data" name="data" required><br>
        
        <input type="submit" value="Search">
    </form>
</body>
</html>"""


if __name__ == "__main__": 
    app.run(debug=True)
