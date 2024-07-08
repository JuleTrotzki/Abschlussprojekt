
# from turtle import home
# import streamlit as st
# from ekg_anzeige import display_sensitive_data
# from login import login
# import add_person
# import home



# # Streamlit App
# st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# if 'threshold' not in st.session_state:
#     st.session_state.threshold = 345
# if 'start_index' not in st.session_state:
#     st.session_state.start_index = 0
# if 'end_index' not in st.session_state:
#     st.session_state.end_index = None
# if 'sampling_rate' not in st.session_state:
#     st.session_state.sampling_rate = 1000
# if 'smooth_window_size' not in st.session_state:
#     st.session_state.smooth_window_size = 100
# if 'authenticated' not in st.session_state:
#     st.session_state['authenticated'] = False

    
# st.sidebar.title("Menü")
# menu = st.sidebar.radio("Seiten", ["Home", "Login", "EKG Daten", "Neue Person anlegen"])


# if menu == "Home":
#     home.show_home_page()  # Aufruf der Funktion zur Anzeige der Home-Seite
    

# elif menu == "Login":
#     if not st.session_state['authenticated']:
#         login()
#     else:
#         st.success("Du bist bereits eingeloggt!")
#         st.write("Wechsle zu den geheimen Daten über die Navigation.")
        
# elif menu == "EKG Daten":
#     if st.session_state['authenticated']:
#         display_sensitive_data()
#     else:
#         st.warning("Bitte logge dich zuerst ein, um diese Seite zu sehen.")
        
# elif menu == "Neue Person anlegen":
#     if st.session_state['authenticated']:
#         add_person.add_person()
#     else:
#         st.warning("Bitte logge dich zuerst ein, um eine neue Person anzulegen.")


import streamlit as st
from ekg_anzeige import display_sensitive_data
from login import show_login_page
from add_person import add_person
from home import show_home_page
from streamlit_option_menu import option_menu

# Streamlit App Configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Initialize session state variables
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

# Sidebar Language Selection
st.sidebar.title("Sprache / Language")
language = option_menu(
    menu_title=None,  # required
    options=["Deutsch", "English"],  # required
    icons=["flag", "flag"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

# Update session state with selected language
st.session_state.language = language

# Sidebar Navigation
st.sidebar.title("Menü")
menu = st.sidebar.radio("Seiten", ["Home", "Login", "EKG Daten", "Neue Person anlegen"])

# Update session state with selected page
if menu == "Home":
    st.session_state.page = 'Home'
elif menu == "Login":
    st.session_state.page = 'Login'
elif menu == "EKG Daten":
    st.session_state.page = 'EKG Daten'
elif menu == "Neue Person anlegen":
    st.session_state.page = 'Neue Person anlegen'

# Function to get text based on selected language
def get_text(texts):
    return texts[st.session_state.language]

# Page Rendering
if st.session_state.page == "Home":
    show_home_page(get_text)  # Pass get_text function to display the home page

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



