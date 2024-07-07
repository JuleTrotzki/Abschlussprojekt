import streamlit as st 


# Eine Liste mit gültigen Benutzern und Passwörtern
VALID_USERS = {"admin": "admin123", "user1": "password1", "1":"1"}

# Session State initialisieren
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Funktion zur Authentifizierung des Benutzers
def authenticate(username, password):
    return VALID_USERS.get(username) == password


def login():
    st.title("Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.success("Login erfolgreich!")
            st.sidebar.write("Willkommen, " + username + "!")
        else:
            st.error("Ungültiger Benutzername oder Passwort")