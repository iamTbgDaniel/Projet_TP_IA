import mysql.connector
from database import get_db_connection
from phishing_detector import is_phishing

# Fonction pour envoyer un message
def send_message(sender, receiver, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    phishing = is_phishing(message)
    cursor.execute("INSERT INTO messages (sender, receiver, message, is_phishing) VALUES (%s, %s, %s, %s)", 
                   (sender, receiver, message, phishing))
    conn.commit()
    conn.close()

# Fonction pour récupérer les messages reçus
def get_messages(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message, is_phishing FROM messages WHERE receiver = %s ORDER BY timestamp DESC", (user,))
    messages = cursor.fetchall()
    conn.close()
    return messages
