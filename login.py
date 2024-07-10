import streamlit as st

# Eine Liste mit gültigen Benutzern und Passwörtern
VALID_USERS = {"admin": "admin123", "user1": "password1", "1": "1"}

# Funktion zur Authentifizierung des Benutzers
def authenticate(username, password):
    return VALID_USERS.get(username) == password

def show_login_page(get_text):
    """
    Diese Funktion zeigt die Login-Seite der Anwendung an und ermöglicht es Benutzern,
    sich mit ihrem Benutzernamen und Passwort anzumelden.
    """

    # Setzt den Titel der Seite auf "Login" basierend auf der ausgewählten Sprache
    st.title(get_text({"Deutsch": "Login", "English": "Login"}))

    # Eingabefeld für den Benutzernamen
    username = st.text_input(get_text({"Deutsch": "Benutzername", "English": "Username"}))

    # Eingabefeld für das Passwort, das Eingabefeld ist vom Typ "password", sodass das Passwort verborgen bleibt
    password = st.text_input(get_text({"Deutsch": "Passwort", "English": "Password"}), type="password")

    # Login-Button
    if st.button(get_text({"Deutsch": "Login", "English": "Login"})):
        # Überprüft die Authentifizierung mit den eingegebenen Anmeldeinformationen
        if authenticate(username, password):
            # Setzt den Authentifizierungsstatus in der Session auf True
            st.session_state['authenticated'] = True
            
            # Zeigt eine Erfolgsmeldung an
            st.success(get_text({"Deutsch": "Login erfolgreich!", "English": "Login successful!"}))
            
            # Zeigt den Benutzernamen in der Seitenleiste an
            st.sidebar.write(get_text({"Deutsch": "Willkommen, ", "English": "Welcome, "}) + username + "!")
            
            # Wechselt zur Seite 'EKG Daten'
            st.session_state.page = 'EKG Daten'
        else:
            # Zeigt eine Fehlermeldung bei ungültigen Anmeldeinformationen an
            st.error(get_text({"Deutsch": "Ungültiger Benutzername oder Passwort", "English": "Invalid username or password"}))

if __name__ == "__main__":
    show_login_page()

