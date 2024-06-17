import streamlit as st
from person import Person
from ekgdata_jule import EKGdata
import plotly.graph_objs as go


if 'threshold' not in st.session_state:
    st.session_state.threshold = 345
if 'start_index' not in st.session_state:
    st.session_state.start_index = 0
if 'end_index' not in st.session_state:
    st.session_state.end_index = 10000
if 'sampling_rate' not in st.session_state:
    st.session_state.sampling_rate = 1000
if 'smooth_window_size' not in st.session_state:
    st.session_state.smooth_window_size = 100



# Laden der Personendaten
person_data = Person.load_person_data()
person_list = Person.get_person_list(person_data)

# Titel der App
st.title("EKG Data Analysis App")

# Auswahl der Person
selected_person_name = st.selectbox("Wähle eine Person aus:", person_list)
selected_person_data = Person.find_person_data_by_name(selected_person_name)

# Anzeige der Personendaten
if selected_person_data:
    person = Person(selected_person_data)
    
    if person.picture_path:
        col1, col2 = st.columns([1, 2])
    with col1:
        st.image(person.picture_path,caption=f"{person.firstname} {person.lastname}", width=200)
    with col2:
        st.write(f"Name: {person.firstname} {person.lastname}")
        st.write(f"Geburtsjahr: {person.date_of_birth}")
        st.write(f"Maximale Herzfrequenz: {person.calc_max_heart_rate()} bpm")
    
    # Auswahl des EKG-Tests
    ekg_test_list = [f"Test ID: {test['id']} - Datum: {test['date']}" for test in selected_person_data["ekg_tests"]]
    selected_ekg_test = st.selectbox("Wähle einen EKG-Test aus:", ekg_test_list)
    
    if selected_ekg_test:
        selected_test_id = int(selected_ekg_test.split()[2])
        ekg_test_data = EKGdata.load_by_id(selected_test_id)
        
        if ekg_test_data:
            ekg = EKGdata(ekg_test_data)
            
            # Ermittlung der Peaks
            peaks = EKGdata.find_peaks(ekg.df['EKG in mV'], st.session_state.threshold)
            
            # Berechnung der Herzfrequenz
            heart_rates_df = EKGdata.calculate_HR(peaks, st.session_state.sampling_rate, st.session_state.smooth_window_size)
            
            # Plot der EKG Daten
            fig = EKGdata.plot_time_series(ekg.df, peaks, st.session_state.start_index, st.session_state.end_index)
            st.plotly_chart(fig)
            
            # Plot der Herzfrequenz
            heart_rate_fig = go.Figure()
            heart_rate_fig.add_trace(go.Scatter(
                x=heart_rates_df['Zeitpunkt'], 
                y=heart_rates_df['Herzfrequenz'],
                mode='lines',
                name='Herzfrequenz'))
                
            heart_rate_fig.update_layout(
                title='Herzfrequenz über die Zeit',
                xaxis_title='Zeitpunkt (ms)',
                yaxis_title='Herzfrequenz (Schläge pro Minute)',
                showlegend=True)
            st.plotly_chart(heart_rate_fig)
            
            # Eingabe threshold, start_index und end_index
            st.session_state.threshold = st.slider("Wähle den Schwellenwert für die Peaks:", min_value=0, max_value=1000, value=345)
            st.session_state.end_index = st.slider("Wähle die Länge des zu betrachtenden Zeitbereichs:", min_value=0, max_value=len(ekg.df), value=10000)
            st.session_state.sampling_rate = st.slider("Wähle die Abtastrate:", min_value=1, max_value=10000, value=1000)
            st.session_state.smooth_window_size = st.slider("Wähle die Auflösung der Herzfrequenz-Anzeige:", min_value=1, max_value=1000, value=100)
 
else:
    st.write("Keine Daten für die ausgewählte Person gefunden.")