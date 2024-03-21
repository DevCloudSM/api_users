import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

USER_FILE = "C:\\Users\\aronn\\OneDrive\\Desktop\\2eme année\\devcloud\\sae 401\\users.json"

try:
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump([], f)
except Exception as e:
    print("Erreur lors de la création du fichier utilisateur.json:", e)

# Route pour obtenir tous les utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    return jsonify(users)

# Route pour obtenir un utilisateur par son ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return "User not found", 404

# Route pour ajouter un utilisateur
@app.route("/users", methods=["POST"])
def create_user():
    if not request.json:
        return jsonify({'error': 'No Data'}), 400

    user_data = request.json

    with open(USER_FILE, "r") as f:
        users = json.load(f)

    # Générer un nouvel ID pour l'utilisateur
    user_data["id"] = len(users) + 1

    # Ajouter le nouvel utilisateur aux données existantes
    users.append(user_data)

    # Écrire les données mises à jour dans le fichier JSON
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return jsonify(user_data), 201


# Route pour mettre à jour un utilisateur par son ID
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user_data = request.json
    if not user_data:
        return jsonify({'error': 'No Data'}), 400
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    for user in users:
        if user["id"] == user_id:
            user.update(user_data)
            with open(USER_FILE, "w") as f:
                json.dump(users, f, indent=4)
            return jsonify(user), 200
    return "User not found", 404

# Route pour supprimer un utilisateur par son ID
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    updated_users = [user for user in users if user["id"] != user_id]
    if len(users) == len(updated_users):
        return "User not found", 404
    with open(USER_FILE, "w") as f:
        json.dump(updated_users, f, indent=4)
    return "", 204

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestion des utilisateurs</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Gestion des utilisateurs</h1>

        <h2>Ajouter un utilisateur</h2>
        <form id="addUserForm">
            <label for="nom">Nom:</label>
            <input type="text" id="nom" name="nom"><br><br>
            <label for="prenom">Prénom:</label>
            <input type="text" id="prenom" name="prenom"><br><br>
            <label for="mail">Email:</label>
            <input type="email" id="mail" name="mail"><br><br>
            <label for="telephone">Téléphone:</label>
            <input type="text" id="telephone" name="telephone"><br><br>
            <input type="submit" value="Ajouter">
        </form>

        <h2>Modifier un utilisateur</h2>
        <form id="updateUserForm">
            <label for="userId">ID de l'utilisateur:</label>
            <input type="number" id="userId" name="userId"><br><br>
            <label for="newNom">Nouveau nom:</label>
            <input type="text" id="newNom" name="newNom"><br><br>
            <label for="newPrenom">Nouveau prénom:</label>
            <input type="text" id="newPrenom" name="newPrenom"><br><br>
            <label for="newMail">Nouvel email:</label>
            <input type="email" id="newMail" name="newMail"><br><br>
            <label for="newTelephone">Nouveau téléphone:</label>
            <input type="text" id="newTelephone" name="newTelephone"><br><br>
            <input type="submit" value="Modifier">
        </form>

        <h2>Supprimer un utilisateur</h2>
        <form id="deleteUserForm">
            <label for="deleteUserId">ID de l'utilisateur à supprimer:</label>
            <input type="number" id="deleteUserId" name="deleteUserId"><br><br>
            <input type="submit" value="Supprimer">
        </form>

        <h2>Chercher un utilisateur</h2>
        <form id="searchUserForm">
            <label for="searchUserId">ID de l'utilisateur:</label>
            <input type="number" id="searchUserId" name="searchUserId"><br><br>
            <input type="submit" value="Chercher">
        </form>

        <div id="userResult"></div>

        <script>
            $(document).ready(function() {
                // Fonction pour ajouter un utilisateur
                $("#addUserForm").submit(function(event) {
                    event.preventDefault();
                    var formData = $(this).serialize();
                    $.post("/users", formData, function(data) {
                        alert("Utilisateur ajouté avec succès");
                    });
                });

                // Fonction pour modifier un utilisateur
                $("#updateUserForm").submit(function(event) {
                    event.preventDefault();
                    var formData = $(this).serialize();
                    $.ajax({
                        url: "/users/" + $("#userId").val(),
                        type: "PUT",
                        data: formData,
                        success: function(data) {
                            alert("Utilisateur modifié avec succès");
                        }
                    });
                });

                // Fonction pour supprimer un utilisateur
                $("#deleteUserForm").submit(function(event) {
                    event.preventDefault();
                    $.ajax({
                        url: "/users/" + $("#deleteUserId").val(),
                        type: "DELETE",
                        success: function(data) {
                            alert("Utilisateur supprimé avec succès");
                        }
                    });
                });

                // Fonction pour chercher un utilisateur
                $("#searchUserForm").submit(function(event) {
                    event.preventDefault();
                    $.get("/users/" + $("#searchUserId").val(), function(data) {
                        $("#userResult").html(data);
                    });
                });
            });
        </script>
    </body>
    </html>
    """
if __name__ == "__main__":
    app.run(port=5000)
