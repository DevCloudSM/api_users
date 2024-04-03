# Documentation de l'API Utilisateurs

Cette documentation décrit le fonctionnement de l'API Flask Utilisateur et ses différents endpoints.

## Introduction

L'API Utilisateur est conçue pour gérer les opérations CRUD (Create, Read, Update, Delete) sur une liste d'utilisateurs. Elle prend en charge les requêtes HTTP POST, GET, PATCH et DELETE pour interagir avec les données des utilisateurs.

## Endpoints

### Accueil (`GET /`)

- **Description :** Affiche la page d'accueil de l'API.
- **Fonction :** `accueil()`
- **Type de Requête :** GET
- **Paramètres :** Aucun
- **Réponse :** _(Interface graphique)_ Renvoie une page HTML contenant un lien vers chaque endpoint.

### Ajouter un Utilisateur (`GET /user`, `POST /user`)

- **Description :** Permet d'ajouter un nouvel utilisateur soit directement via une requête, soit par l'interface graphique.
- **Fonction :** `affichage_user()`, `post_user()`
- **Types de Requête :** GET, POST
- **Paramètres (POST) :** Nom, prénom, nom d'utilisateur, email
- **Réponse (POST) :** Renvoie les données de l'utilisateur ajouté au format JSON 
- **Réponse (GET) :** _(Interface graphique)_ Renvoi une page HTML selon le Content-Type de la requête.

### Obtenir un Utilisateur (`GET /user/<int:userId>`)

- **Description :** Récupère les informations d'un utilisateur spécifié par son ID.
- **Fonction :** `get_user(userId)`
- **Type de Requête :** GET
- **Paramètres :** ID de l'utilisateur
- **Réponse :** Renvoie les données de l'utilisateur au format JSON.

### Modifier un Utilisateur (`POST /user/modify`, `PATCH /user/<int:userId>`)

- **Description :** Permet de modifier les informations d'un utilisateur existant.
- **Fonction :** `recovery_of_user_to_modify()`, `modification_user(userId)`
- **Types de Requête :** POST, PATCH
- **Paramètres (POST) :** _(Interface graphique)_ Critères de recherche entré par l'interface graphique (nom, prénom, nom d'utilisateur, email)
- **Paramètres (PATCH) :** ID de l'utilisateur à modifier et les nouvelles données récupèré par l'interface graphique ou une requête json.
- **Réponse :** Renvoie un message de succès ou d'erreur de la modification.

### Supprimer un Utilisateur (`GET /user/delete`, `POST /user/delete/result`, `DELETE /user/<int:userId>`)

- **Description :** Permet de supprimer un utilisateur existant soit directement via une requête, soit par l'interface graphique.
- **Fonction :** `suppression_user_interface()`, `affichage_donnée_delete()`, `suppression_user(userId)`
- **Types de Requête :** GET, POST, DELETE
- **Paramètres (POST) :** ID de l'utilisateur à supprimer
- **Réponse (GET) :** _(Interface graphique)_ Renvoie une page de l'interface de suppression.
- **Réponse (DELETE) :** Renvoie un message de succès ou d'erreur de la suppression.

### Rechercher des Utilisateurs (`GET /user/findby/search`, `POST /user/findby/result`, `GET /user/findby`)

- **Description :** Permet de rechercher des utilisateurs en fonction de différents critères.
- **Fonction :** `find_user_by_interface()`, `find_user_by_interface_result()`, `get_user_findby()`
- **Types de Requête :** GET, POST
- **Paramètres (POST) :** _(Interface graphique)_ Critères de recherche (nom, prénom, nom d'utilisateur, email)
- **Paramètres (GET) :** Critères de recherche (ID, nom, prénom, nom d'utilisateur, email)
- **Réponse :** Renvoie une liste d'utilisateurs correspondant aux critères de recherche.

### Afficher tous les Utilisateurs (`GET /affichage`)

- **Description :** Affiche tous les utilisateurs enregistrés.
- **Fonction :** `affichage()`
- **Type de Requête :** GET
- **Paramètres :** Aucun
- **Réponse :** _(Interface graphique)_ Renvoie une page HTML contenant la liste de tous les utilisateurs.
