import streamlit as st
import pickle
import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Charger le modèle et le vecteur sauvegardé
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Fonction de nettoyage des emails
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Fonction pour prédire si l'email est phishing ou safe
def predict_email(text):
    cleaned_text = clean_text(text)
    vectorized_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vectorized_text)
    return prediction[0]

# Interface Streamlit
st.title("Email Classifier: Phishing or Safe?")
st.write("Entrez le texte d'un email pour vérifier s'il est **phishing** ou **safe**.")

# Zone de texte pour que l'utilisateur entre un email
email_text = st.text_area("Email à analyser", height=250)

# Bouton de prédiction
if st.button("Classer l'email"):
    if email_text:
        # Classifier l'email
        result = predict_email(email_text)
        if result == 0:
            st.success("Cet email est **safe**.")
        else:
            st.error("Cet email est **phishing** ou **spam**.")
    else:
        st.warning("Veuillez entrer un email à analyser.")
