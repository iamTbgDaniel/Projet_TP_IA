import mysql.connector

# Connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Modifier avec ton utilisateur MySQL
        password="",  # Ajouter ton mot de passe MySQL
        database="messaging_app"
    )
