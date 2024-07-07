import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from login import authenticate, login

def show_home_page():
    st.title("Home")
    
    # Titel der App und Logo
    col1, col2 = st.columns([3, 1])
    with col1:
        rgb_value = (206, 21, 76)
        st.markdown(
            f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">Beat Analyzer</h1></div>',
            unsafe_allow_html=True)
    with col2:
        st.image('Logo.png')

    #Einleitungstext
    st.write("""
    Willkommen bei **Beat Analyzer** – Ihrer umfassenden Plattform zur Analyse und Überwachung Ihrer Herzfrequenz. 
    Entdecken Sie detaillierte Einblicke in Ihre Herzgesundheit und nutzen Sie unsere benutzerfreundlichen Tools, 
    um Ihr Wohlbefinden zu optimieren.
    """)

    st.write("### Funktionen der App")
    if st.button('-Login'):
        st.session_state['page'] = 'login'
        st.rerun()
    st.write("-lade deine Trainingsdaten hoch")
    st.write("-lass deine Daten auswerten und in einem Diagramm anzeigen")


