
import streamlit as st
from ekg_anzeige import display_sensitive_data
from login import login
import add_person



# Streamlit App
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

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

    
st.sidebar.title("Menü")
menu = st.sidebar.radio("Seiten", ["Home", "Login", "EKG Daten", "Neue Person anlegen"])

if menu == "Home":
    st.title("Home")
    st.write("Willkommen auf der Home-Seite. Hier findest du allgemeine Informationen über die App.")

elif menu == "Login":
    if not st.session_state['authenticated']:
        login()
    else:
        st.success("Du bist bereits eingeloggt!")
        st.write("Wechsle zu den geheimen Daten über die Navigation.")
        
elif menu == "EKG Daten":
    if st.session_state['authenticated']:
        display_sensitive_data()
    else:
        st.warning("Bitte logge dich zuerst ein, um diese Seite zu sehen.")
        
elif menu == "Neue Person anlegen":
    if st.session_state['authenticated']:
        add_person.add_person()
    else:
        st.warning("Bitte logge dich zuerst ein, um eine neue Person anzulegen.")




