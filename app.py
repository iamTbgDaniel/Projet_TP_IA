# app.py - Fichier principal Streamlit
import streamlit as st
from auth import login_user, register_user
from messaging import send_message, get_messages

st.title("Application de Messagerie")

menu = ["Connexion", "Inscription", "Messagerie"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Inscription":
    st.subheader("Créer un compte")
    new_user = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Mot de passe", type="password")
    if st.button("S'inscrire"):
        if register_user(new_user, new_password):
            st.success("Inscription réussie! Vous pouvez maintenant vous connecter.")
            st.session_state["menu"] = "Connexion"
            st.rerun()
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
            st.session_state["menu"] = "Messagerie"
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader(f"Bienvenue, {st.session_state['username']}")
    
    receiver = st.text_input("Envoyer un message à")
    message = st.text_area("Votre message")
    if st.button("Envoyer"):
        if receiver and message:
            send_message(st.session_state['username'], receiver, message)
            st.success("Message envoyé!")
        else:
            st.error("Veuillez remplir tous les champs.")
    
    st.subheader("Messages reçus")
    messages = get_messages(st.session_state['username'])
    for sender, message, phishing in messages:
        if phishing:
            st.error(f"{sender}: {message} (⚠️ Phishing détecté!)")
        else:
            st.info(f"{sender}: {message}")
else:
    st.warning("Veuillez vous connecter pour accéder à la messagerie.")
