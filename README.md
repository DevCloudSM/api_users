# API_Utilisateurs

## Contenue de la base de donnée de l'API utilisateur : 

**Base de donnée utilisateur (Accessible par toutes la API) :**
 - ID
 - Surname
 - Name
 - Username
 - Mail

## Objectif de l'API Utilisateur :

L'API Utilisateur a pour objectif de fournir des fonctionnalités permettant aux applications de gérer les profils des utilisateurs, y compris la création, la récupération, la mise à jour et la suppression des informations utilisateur.

**Principaux objectifs de l'API Utilisateur :**

1. Créer un utilisateur : Permettre d'enregistrer de nouveaux utilisateurs en fournissant les informations nécessaires telles que :
      nom; prenom; pseudo; mail; id
   Idées (S'il reste du temps):
      adresse; pays; départements ( dans l'entreprise ); entreprises; PP; descriptions
   
3. Créer des utilisateurs de façon aléatoire.

4. Supprimer un utilisateur : Permettre aux applications de supprimer un utilisateur spécifique de la base de données, le cas échéant.
   
5. Récupérer les informations d'un utilisateur : méthode pour récupérer les détails d'un utilisateur spécifique en fonction de son identifiant unique ou d'autres critères de recherche.
      - Fonction recherche avec différent attribut de recherche (Comme nom,prénom...)

7. Mettre à jour les informations d'un utilisateur : Autoriser les applications à mettre à jour les informations d'un utilisateur existant, telles que le nom, l'adresse e-mail, etc.

8. Gestion des autorisations et des rôles : Intégrer des fonctionnalités pour gérer les autorisations et les rôles des utilisateurs, en permettant par exemple aux administrateurs de définir les privilèges d'accès des utilisateurs.
