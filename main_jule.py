import streamlit as st
from ekg_anzeige import display_sensitive_data
from login import show_login_page
from add_person import add_person
from home import show_home_page
from streamlit_option_menu import option_menu

# Konfiguration der Streamlit-App
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Initialisieren von Session-State-Variablen
if 'threshold' not in st.session_state:
    st.session_state.threshold = 345
if 'start_index' not in st.session_state:
    st.session_state.start_index = 0
if 'end_index' not in st.session_state:
    st.session_state.end_index = None
if 'sampling_rate' not in st.session_state:
    st.session_state.sampling_rate = 1000
if 'smooth_window_size' not in st.session_state:
    st.session_state.smooth_window_size = 100
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'language' not in st.session_state:
    st.session_state.language = 'Deutsch'
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Seitenauswahl für Sprache in der Seitenleiste
st.sidebar.title("Sprache / Language")
language = option_menu(
    menu_title=None,  # erforderlich
    options=["Deutsch", "English"],  # erforderlich
    icons=["flag", "flag"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

# Aktualisieren des Session-State mit der ausgewählten Sprache
st.session_state.language = language

# Funktion, um Text basierend auf der ausgewählten Sprache zu erhalten
def get_text(texts):
    return texts[st.session_state.language]

# Navigation in der Seitenleiste
st.sidebar.title(get_text({"Deutsch": "Menü", "English": "Menu"}))
menu = st.sidebar.radio(get_text({"Deutsch": "Seiten", "English": "Pages"}), [
    get_text({"Deutsch": "Home", "English": "Home"}),
    get_text({"Deutsch": "Login", "English": "Login"}),
    get_text({"Deutsch": "EKG Daten", "English": "EKG Data"}),
    get_text({"Deutsch": "Neue Person anlegen", "English": "Add New Person"})
])

# Aktualisieren des Session-State mit der ausgewählten Seite
if menu == get_text({"Deutsch": "Home", "English": "Home"}):
    st.session_state.page = 'Home'
elif menu == get_text({"Deutsch": "Login", "English": "Login"}):
    st.session_state.page = 'Login'
elif menu == get_text({"Deutsch": "EKG Daten", "English": "EKG Data"}):
    st.session_state.page = "EKG Daten"
elif menu == get_text({"Deutsch": "Neue Person anlegen", "English": "Add New Person"}):
    st.session_state.page = "Neue Person anlegen"

# Seitenanzeige basierend auf der aktuellen Seitenauswahl
if st.session_state.page == "Home":
    show_home_page(get_text)  # Übergeben der get_text-Funktion, um die Startseite anzuzeigen

elif st.session_state.page == "Login":
    if not st.session_state['authenticated']:
        show_login_page(get_text)
    else:
        st.success(get_text({"Deutsch": "Du bist bereits eingeloggt!", "English": "You are already logged in!"}))
        st.write(get_text({"Deutsch": "Wechsle zu den geheimen Daten über die Navigation.", "English": "Navigate to the secret data using the sidebar."}))

elif st.session_state.page == "EKG Daten":
    if st.session_state['authenticated']:
        display_sensitive_data(get_text)
    else:
        st.warning(get_text({"Deutsch": "Bitte logge dich zuerst ein, um diese Seite zu sehen.", "English": "Please log in first to view this page."}))

elif st.session_state.page == "Neue Person anlegen":
    if st.session_state['authenticated']:
        add_person(get_text)
    else:
        st.warning(get_text({"Deutsch": "Bitte logge dich zuerst ein, um eine neue Person anzulegen.", "English": "Please log in first to add a new person."}))
