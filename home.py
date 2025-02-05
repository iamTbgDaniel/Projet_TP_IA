import streamlit as st
import mysql.connector
from hashlib import sha256

# Connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Modifier avec votre utilisateur MySQL
        password="",  # Ajouter votre mot de passe MySQL
        database="messaging_app"
    )

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

# Interface Streamlit
st.title("Application de Messagerie - Connexion et Inscription")

menu = ["Connexion", "Inscription"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Inscription":
    st.subheader("Créer un compte")
    new_user = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Mot de passe", type="password")
    if st.button("S'inscrire"):
        if register_user(new_user, new_password):
            st.success("Inscription réussie! Vous pouvez maintenant vous connecter.")
        else:
            st.error("Nom d'utilisateur déjà pris.")

elif choice == "Connexion":
    st.subheader("Se connecter")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if login_user(username, password):
            st.success(f"Bienvenue {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")