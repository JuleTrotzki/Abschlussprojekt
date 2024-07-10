import streamlit as st
from person import Person
from ekgdata import EKGdata
import plotly.graph_objs as go
import os

def display_sensitive_data(get_text):
    """
    Zeigt sensible Daten, einschließlich EKG-Daten und persönlicher Informationen, in einer Streamlit-App an.
    """
    # Laden der Personendaten
    person_data = Person.load_person_data()
    person_list = Person.get_person_list(person_data)

    # Titel der App und Logo
    col1, col2 = st.columns([3, 1])
    with col1:
        rgb_value = (206, 21, 76)
        st.markdown(
            f'<div style="background-color: rgb{rgb_value}; padding: 10px; margin-top: 60px;"><h1 style="color: white; margin-top: 0;">{get_text({"Deutsch": "Beat Analyzer", "English": "Beat Analyzer"})}</h1></div>',
            unsafe_allow_html=True)
    with col2:
        st.image('Logo.png')

    # Auswahl der Person
    with st.sidebar:
        st.header(get_text({"Deutsch": "Personenauswahl", "English": "Select Person"}))
        selected_person_name = st.selectbox(get_text({"Deutsch": "Wähle eine Person aus:", "English": "Choose a person:"}), person_list)
        selected_person_data = Person.find_person_data_by_name(selected_person_name)

        if selected_person_data:
            ekg_test_list = [f"Test ID: {test['id']} - Datum: {test['date']}" for test in selected_person_data["ekg_tests"]]
            selected_ekg_test = st.selectbox(get_text({"Deutsch": "Wähle einen EKG-Test aus:", "English": "Choose an EKG test:"}), ekg_test_list)

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
                st.write(f"**{get_text({'Deutsch': 'Name', 'English': 'Name'})}:** {person.firstname} {person.lastname}")
                st.write(f"**{get_text({'Deutsch': 'Geburtsjahr', 'English': 'Birth Year'})}:** {person.date_of_birth}")
                st.write(f"**{get_text({'Deutsch': 'Maximale Herzfrequenz', 'English': 'Max Heart Rate'})}:** {person.calc_max_heart_rate()} bpm")

        if selected_ekg_test:
            selected_test_id = int(selected_ekg_test.split()[2])
            ekg_test_data = EKGdata.load_by_id(selected_test_id)
            
            if ekg_test_data:
                ekg_data = EKGdata(ekg_test_data)
                st.subheader(get_text({"Deutsch": "EKG-Daten", "English": "EKG Data"}))

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

                            hrv_metrics = EKGdata.calculate_HRV(peaks, st.session_state.sampling_rate)
                            
                            heart_rate_fig = go.Figure()
                            heart_rate_fig.add_trace(go.Scatter(
                                x=heart_rate_df['Zeitpunkt'],
                                y=heart_rate_df['Herzfrequenz'],
                                mode='lines',
                                name=get_text({'Deutsch': 'Herzfrequenz', 'English': 'Heart Rate'})
                            ))

                            heart_rate_fig.update_layout(
                                title=get_text({'Deutsch': 'Herzfrequenz', 'English': 'Heart Rate'}),
                                xaxis_title=get_text({'Deutsch': 'Zeit (s)', 'English': 'Time (s)'}),
                                yaxis_title=get_text({'Deutsch': 'Herzfrequenz (Schläge pro Minute)', 'English': 'Heart Rate (BPM)'}),
                                showlegend=True
                            )
                            st.plotly_chart(heart_rate_fig)
                            
                            # Anzeige der Herzratenvariabilität
                            st.subheader(get_text({"Deutsch": "Herzratenvariabilität", "English": "Heart Rate Variability"}))
                            st.write(get_text({
                                "Deutsch": "SDNN (Standardabweichung der NN-Intervalle) ist die Standardabweichung der Zeitdifferenzen zwischen aufeinanderfolgenden Herzschlägen (RR-Intervalle). Sie repräsentiert die Gesamtvariabilität der Herzfrequenz über einen bestimmten Zeitraum und ist ein allgemeines Maß für die HRV.",
                                "English": "SDNN (Standard Deviation of the NN Interval) is the standard deviation of the time differences between consecutive heartbeats (RR intervals). It represents the overall variability of heart rate over a certain period and is a general measure of HRV."}))
                            st.write(f"**SDNN**: {hrv_metrics['SDNN']:.2f} s")
                            st.write(get_text({
                                "Deutsch": "RMSSD (Quadratwurzel des Mittelwerts der quadrierten Differenzen) ist einer der wichtigsten Parameter, der Auskunft über die Aktivität des Parasympathikus gibt. Er beschreibt die kurzzeitige Variabilität des Herzschlags, wie stark sich die Herzfrequenz von einem zum nächsten Herzschlag ändert.",
                                "English": "RMSSD (Root Mean Square of Successive Differences) is one of the key parameters that provides information about parasympathetic activity. It describes the short-term variability of the heartbeat, indicating how much the heart rate changes from one beat to the next."}))
                            st.write(f"**RMSSD**: {hrv_metrics['RMSSD']:.2f} s")
                            st.write(get_text({
                                "Deutsch": "NN50 ist die Anzahl der Paare von RR-Intervallen, die mehr als 50ms auseinander liegen.",
                                "English": "NN50 is the number of pairs of RR intervals that are more than 50ms apart."}))
                            st.write(f"**NN50**: {hrv_metrics['NN50']}")
                            st.write(get_text({
                                "Deutsch": "pNN50 ist der Prozentsatz an Paaren von RR-Intervallen, die mehr als 50ms auseinander liegen.",
                                "English": "pNN50 is the percentage of pairs of RR intervals that are more than 50ms apart."}))
                            st.write(f"**pNN50**: {hrv_metrics['PNN50']:.2f} %")
                            
                            
                        # Eingabe end_index
                        with col2:
                            with st.expander(get_text({"Deutsch": "Zeitbereich auswählen", "English": "Select Time Range"})):
                                st.session_state.end_index = st.slider(
                                    get_text({"Deutsch": "Wähle die Länge des Zeitbereichs:", "English": "Select the length of the time range:"}), 
                                    min_value=0, max_value=len(ekg_data.df), value=5000)

