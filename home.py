# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
# from login import authenticate, login

# def show_home_page():
#     st.title("Home")
    
#     # Titel der App und Logo
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         rgb_value = (206, 21, 76)
#         st.markdown(
#             f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">Beat Analyzer</h1></div>',
#             unsafe_allow_html=True)
#     with col2:
#         st.image('Logo.png')

#     #Einleitungstext
#     st.write("""
#     Willkommen bei **Beat Analyzer** – Ihrer umfassenden Plattform zur Analyse und Überwachung Ihrer Herzfrequenz. 
#     Entdecken Sie detaillierte Einblicke in Ihre Herzgesundheit und nutzen Sie unsere benutzerfreundlichen Tools, 
#     um Ihr Wohlbefinden zu optimieren.
#     """)

#     st.write("### Funktionen der App")
#     if st.button('-Login'):
#         st.session_state['page'] = 'login'
#         st.rerun()
#     st.write("-lade deine Trainingsdaten hoch")
#     st.write("-lass deine Daten auswerten und in einem Diagramm anzeigen")


# import streamlit as st

# def show_home_page(get_text):
    

#     # Title and Logo
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         rgb_value = (206, 21, 76)
#         st.markdown(
#             f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">Beat Analyzer</h1></div>',
#             unsafe_allow_html=True)
#     with col2:
#         st.image('Logo.png')

#     st.title(get_text({"Deutsch": "Home", "English": "Home"}))

#     # Introduction text
#     st.write(get_text({
#         "Deutsch": "Willkommen bei **Beat Analyzer** – Ihrer umfassenden Plattform zur Analyse und Überwachung Ihrer Herzfrequenz. Entdecken Sie detaillierte Einblicke in Ihre Herzgesundheit und nutzen Sie unsere benutzerfreundlichen Tools, um Ihr Wohlbefinden zu optimieren.",
#         "English": "Welcome to **Beat Analyzer** – your comprehensive platform for analyzing and monitoring your heart rate. Discover detailed insights into your heart health and use our user-friendly tools to optimize your well-being."
#     }))

#     st.write("### " + get_text({"Deutsch": "Funktionen der App", "English": "App Features"}))
#     if st.button(get_text({"Deutsch": "Login", "English": "Login"})):
#         st.session_state.page = 'Login'
#     st.write(get_text({"Deutsch": "- Lade deine Trainingsdaten hoch", "English": "- Upload your training data"}))
#     st.write(get_text({"Deutsch": "- Lass deine Daten auswerten und in einem Diagramm anzeigen", "English": "- Analyze your data and display it in a chart"}))

# if __name__ == "__main__":
#     show_home_page()

import streamlit as st
from login import show_login_page
from login import VALID_USERS, authenticate



def show_home_page(get_text):

    # Title and Logo
    col1, col2 = st.columns([3, 1])
    with col1:
        rgb_value = (206, 21, 76)
        st.markdown(
            f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">Beat Analyzer</h1></div>',
            unsafe_allow_html=True)
    with col2:
        st.image('Logo.png')


    st.title(get_text({"Deutsch": "Home", "English": "Home"}))

    # Display uploaded image below the logo
    st.image('run.png')
    # Introduction text
    st.write(get_text({
        "Deutsch": "Willkommen bei **Beat Analyzer** – Ihrer umfassenden Plattform zur Analyse und Überwachung Ihrer Herzfrequenz. Entdecken Sie detaillierte Einblicke in Ihre Herzgesundheit und nutzen Sie unsere benutzerfreundlichen Tools, um Ihr Wohlbefinden zu optimieren.",
        "English": "Welcome to **Beat Analyzer** – your comprehensive platform for analyzing and monitoring your heart rate. Discover detailed insights into your heart health and use our user-friendly tools to optimize your well-being."
    }))

    st.write("### " + get_text({"Deutsch": "Funktionen der App", "English": "App Features"}))
    st.write(get_text({"Deutsch": "- logge dich zuerst ein!", "English": "- first login!"}))
    st.write(get_text({"Deutsch": "- Lade deine Trainingsdaten hoch", "English": "- Upload your training data"}))
    st.write(get_text({"Deutsch": "- Lass deine Daten auswerten und in einem Diagramm anzeigen", "English": "- Analyze your data and display it in a chart"}))

if __name__ == "__main__":
    show_home_page()

