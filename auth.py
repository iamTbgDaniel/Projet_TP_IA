import mysql.connector
from hashlib import sha256
from database import get_db_connection

# Fonction d'inscription
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        conn.close()

# Fonction de connexion
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user
