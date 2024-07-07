import streamlit as st
from person import Person
from ekgdata_jule import EKGdata
import plotly.graph_objs as go
import pandas as pd
import os

def display_sensitive_data():
    # Laden der Personendaten
    person_data = Person.load_person_data()
    person_list = Person.get_person_list(person_data)


    # Titel der App und Logo
    col1, col2 = st.columns([3, 1])
    with col1:
        rgb_value = (206, 21, 76)
        st.markdown(
            f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">Beat Analyzer</h1></div>',
            unsafe_allow_html=True)
    with col2:
        st.image('Logo.png')


    # Auswahl der Person
    with st.sidebar:
        st.header("Personenauswahl")
        selected_person_name = st.selectbox("Wähle eine Person aus:", person_list)
        selected_person_data = Person.find_person_data_by_name(selected_person_name)

        if selected_person_data:
            ekg_test_list = [f"Test ID: {test['id']} - Datum: {test['date']}" for test in selected_person_data["ekg_tests"]]
            selected_ekg_test = st.selectbox("Wähle einen EKG-Test aus:", ekg_test_list)


    # Anzeige der Personendaten und EKG-Daten
    if selected_person_data:
        person = Person(selected_person_data)


        # Bild der Person anzeigen
        if person.picture_path:
            col1, col2, col3 = st.columns([2.5, 0.3, 5])
            with col1:
                st.image(person.picture_path, caption=f"{person.firstname} {person.lastname}", width=200)
                
        # Personendaten anzeigen
            with col2:
                st.image('Name.png', width=25)
                st.image('Geburtsjahr.png', width=25)
                st.image('maxHR.png', width=25)
            with col3:
                st.write(f"**Name:** {person.firstname} {person.lastname}")
                st.write(f"**Geburtsjahr:** {person.date_of_birth}")
                st.write(f"**Maximale Herzfrequenz:** {person.calc_max_heart_rate()} bpm")

        
        if selected_ekg_test:
            selected_test_id = int(selected_ekg_test.split()[2])
            ekg_test_data = EKGdata.load_by_id(selected_test_id)
            
            if ekg_test_data:
                ekg_data = EKGdata(ekg_test_data)
                st.subheader("EKG-Daten")

                file_extension = os.path.splitext(ekg_test_data['result_link'])[1].lower()
                
                if file_extension == '.fit':
                        fit_fig = ekg_data.plot_fit_data(ekg_data.df)
                        st.plotly_chart(fit_fig, use_container_width=True)
                        
                else:
                    if 'EKG in mV' in ekg_data.df.columns:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            peaks = EKGdata.find_peaks(ekg_data.df['EKG in mV'])
                            fig = EKGdata.plot_time_series(ekg_data.df, peaks, st.session_state.start_index, st.session_state.end_index)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Plot der Herzfrequenz
                            heart_rate_df = EKGdata.calculate_HR(peaks, st.session_state.sampling_rate, st.session_state.smooth_window_size)
                        
                            heart_rate_fig = go.Figure()
                            heart_rate_fig.add_trace(go.Scatter(
                                x=heart_rate_df['Zeitpunkt'],
                                y=heart_rate_df['Herzfrequenz'],
                                mode='lines',
                                name='Herzfrequenz'))

                            heart_rate_fig.update_layout(
                                title='Herzfrequenz',
                                xaxis_title='Zeit (s)',
                                yaxis_title='Herzfrequenz (Schläge pro Minute)',
                                showlegend=True)
                            st.plotly_chart(heart_rate_fig)
                            
                        # Eingabe threshold, start_index und end_index
                        with col2:
                            st.session_state.end_index = st.slider("Wähle die Länge des Zeitbereichs:", min_value=0, max_value=len(ekg_data.df), value=5000)
                            #st.session_state.sampling_rate = st.slider("Wähle die Abtastrate:", min_value=1, max_value=10000, value=1000)
                            #st.session_state.smooth_window_size = st.slider("Wähle die Auflösung der Herzfrequenz-Anzeige:", min_value=1, max_value=1000, value=100)
            

                    else:
                        st.warning("Keine gültigen EKG-Daten gefunden.")
                
             
                    

                     
                    
                    
                
            else:
                st.error(f"Keine EKG-Daten für Test ID {selected_test_id} gefunden.")
                
    else:
        st.write("Keine Daten für die ausgewählte Person gefunden.")