import psycopg2 as ps

# Identifiants de connexion à la base de données
identifiants = {
    'database': 'ipam',
    'user': 'postgres',
    'password': 'bonjour',
    'host': 'localhost',
    'port': 5432
}

# Fonction pour ajouter un utilisateur dans la base de données
def ajouter_utilisateur(name, surname, username, email):
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                sql_query = """
                            INSERT INTO public."list_user" (name, surname, username, email)
                            VALUES (%s, %s, %s, %s)
                            """
                cursor.execute(sql_query, (name, surname, username, email))
                connector.commit()
                return True
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'utilisateur : {e}")
        return False

# Fonction pour supprimer un utilisateur de la base de données
def supprimer_utilisateur(user_id):
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                sql_query = """
                            DELETE FROM public."list_user" WHERE id = %s
                            """
                cursor.execute(sql_query, (user_id,))
                connector.commit()
                return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur : {e}")
        return False

# Fonction pour mettre à jour les informations d'un utilisateur dans la base de données
def modifier_utilisateur(user_id, name, surname, username, email):
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                sql_query = """
                            UPDATE public."list_user"
                            SET name = %s, surname = %s, username = %s, email = %s
                            WHERE id = %s
                            """
                cursor.execute(sql_query, (name, surname, username, email, user_id))
                connector.commit()
                return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
        return False

# Fonction pour récupérer tous les utilisateurs de la base de données
def recuperer_utilisateurs():
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                sql_query = """
                            SELECT * FROM public."list_user"
                            """
                cursor.execute(sql_query)
                return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        return None
