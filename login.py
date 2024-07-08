# import streamlit as st 


# # Eine Liste mit gültigen Benutzern und Passwörtern
# VALID_USERS = {"admin": "admin123", "user1": "password1", "1":"1"}

# # Session State initialisieren
# if 'authenticated' not in st.session_state:
#     st.session_state['authenticated'] = False

# # Funktion zur Authentifizierung des Benutzers
# def authenticate(username, password):
#     return VALID_USERS.get(username) == password


# def login():
#     st.title("Login")
#     username = st.text_input("Benutzername")
#     password = st.text_input("Passwort", type="password")

#     if st.button("Login"):
#         if authenticate(username, password):
#             st.session_state['authenticated'] = True
#             st.success("Login erfolgreich!")
#             st.sidebar.write("Willkommen, " + username + "!")
#             st.session_state['page'] = 'ekg_daten'
#             st.experimental_rerun()
#         else:
#             st.error("Ungültiger Benutzername oder Passwort")

import streamlit as st

# Eine Liste mit gültigen Benutzern und Passwörtern
VALID_USERS = {"admin": "admin123", "user1": "password1", "1": "1"}

# Funktion zur Authentifizierung des Benutzers
def authenticate(username, password):
    return VALID_USERS.get(username) == password

def show_login_page(get_text):
    st.title(get_text({"Deutsch": "Login", "English": "Login"}))
    username = st.text_input(get_text({"Deutsch": "Benutzername", "English": "Username"}))
    password = st.text_input(get_text({"Deutsch": "Passwort", "English": "Password"}), type="password")

    if st.button(get_text({"Deutsch": "Login", "English": "Login"})):
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.success(get_text({"Deutsch": "Login erfolgreich!", "English": "Login successful!"}))
            st.sidebar.write(get_text({"Deutsch": "Willkommen, ", "English": "Welcome, "}) + username + "!")
            st.session_state.page = 'EKG Daten'
        else:
            st.error(get_text({"Deutsch": "Ungültiger Benutzername oder Passwort", "English": "Invalid username or password"}))

if __name__ == "__main__":
    show_login_page()
