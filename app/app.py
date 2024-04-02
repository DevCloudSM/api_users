import json, os
from flask import Flask, request, jsonify, Response, render_template
import requests 
from requests.structures import CaseInsensitiveDict
app = Flask(__name__) 
navbar_html = [ {"id":"1", "name":"Home", "url":"/"}, 
                {"id":"2", "name":"Add a user", "url":"/user"},
                {"id":"3", "name":"Modify a user", "url":"/user/modify"},
                {"id":"4", "name":"Find a user", "url":"/user/findby/search"},
                {"id":"5", "name":"Delete a user", "url":"/user/delete"}, 
                {"id":"6", "name":"Show all users", "url":"/test"}]


@app.route("/") 
def accueil(): 
    # Ouvre le fichier index.html lors de la connection à l'api
    return render_template("index.html", navbar=navbar_html)

@app.route('/user')
def affichage_user():
    # Ouvre la page html qui permet à l'utilisateur de remplir le formulaire de création d'utilisateur
    return render_template("add_user.html", navbar=navbar_html)

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

    # Vérifie que toutes les données nécessaires sont présentes
    if not name or not surname or not username or not email:
        return jsonify({"error": "Missing data"}), 400

    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)
    else:
        list_user = []

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
    
    if content_type == 'application/json':
        return Response(json_response, content_type='application/json'), 200
    else:   
        return render_template('add_user_result.html', user=user_data, navbar=navbar_html)

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
    with open('list_user.json', 'r', encoding='utf-8') as f:
        list_user = json.load(f)
    # Recherche de l'utilisateur à modifier
    user = next((a for a in list_user if a['id'] == userId), None)
    if not user:
        return jsonify({"error": "User not find"}), 404

    # Récupération des données JSON de la requête
    data = {} 
    if request.is_json:
        data = request.get_json()

    # Mise à jour des informations de l'utilisateur
    for key, value in data.items():
        user[key] = value

    # Enregistrement de la liste des users modifiée
    with open('list_user.json', 'w', encoding='utf-8') as f:
        json.dump(list_user, f)

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
    if os.path.exists('list_user.json') and os.path.getsize('list_user.json') > 0:
        with open('list_user.json', 'r', encoding='utf-8') as f:
            list_user = json.load(f)

    user_found = False
    for index, user in enumerate(list_user):
        if user['id'] == userId:
            user_found = True
            del list_user[index]
            break

    if not user_found:
        return jsonify({"error": "User non trouvé"}), 404
    
    # Enregistrement du fichier JSON mis à jour
    with open('list_user.json', 'w', encoding='utf-8') as f:
        json.dump(list_user, f, ensure_ascii=False, indent=4)

    return jsonify({}), 204

@app.route('/test', methods=['GET'])
def test():
    # Ouvrir le fichier JSON pour lecture
    with open('list_user.json', 'r', encoding='utf-8') as f:
        try:
            # Charger le contenu JSON
            data = json.load(f)
            return render_template('findby_result.html', navbar=navbar_html, users=data)
            # return jsonify(data), 200
        except json.JSONDecodeError as e:
            # Gérer les erreurs de décodage JSON
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__": 
    app.run(debug=True)