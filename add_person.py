import streamlit as st
import pandas as pd
import json
import os
import datetime as dt
from datetime import datetime

def add_person():
    st.header("Neue Person anlegen")

    firstname = st.text_input("Vorname")
    lastname = st.text_input("Nachname")
    birth_year = st.number_input("Geburtsjahr", min_value=1900, max_value=2100, value=2000, step=1)
    picture_path = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
    ekg_file = st.file_uploader("EKG-Daten hochladen", type=["csv", "txt"])

    if st.button("Person speichern"):
        if not firstname or not lastname or not birth_year:
            st.error("Bitte füllen Sie alle Felder aus!")
            return

        # Speichern des Bildes
        if picture_path:
            picture_dir = "uploaded_pictures"
            os.makedirs(picture_dir, exist_ok=True)
            picture_path_save = os.path.join(picture_dir, picture_path.name)
            with open(picture_path_save, "wb") as f:
                f.write(picture_path.getbuffer())
        else:
            picture_path_save = ""

        # Laden der aktuellen Personendaten
        try:
            with open("data/person_db.json", "r") as file:
                person_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            person_data = []

        # Bestimmen der neuen ID
        new_id = max([person["id"] for person in person_data], default=0) + 1

        # Neue Person hinzufügen
        new_person = {
            "id": new_id,
            "firstname": firstname,
            "lastname": lastname,
            "date_of_birth": str(birth_year),
            "picture_path": picture_path_save,
            "ekg_tests": []  
        }
        person_data.append(new_person)

        # Speichern der aktualisierten Personendaten
        with open("data/person_db.json", "w") as file:
            json.dump(person_data, file, indent=4)

        st.success("Person erfolgreich angelegt!")

        # Speichern der EKG-Daten (falls hochgeladen)
        if ekg_file:
            ekg_dir = "ekg_data"
            os.makedirs(ekg_dir, exist_ok=True)
            ekg_path_save = os.path.join(ekg_dir, f"{ekg_file.name}")
            with open(ekg_path_save, "wb") as f:
                f.write(ekg_file.getbuffer())
                
            for person in person_data:
                if person["id"] == new_id:
                    person["ekg_tests"].append({
                        "id": new_id,
                        "date": datetime.now().strftime('%d.%m.%Y'), 
                        "result_link": ekg_path_save})
            with open("data/person_db.json", "w") as file:
                json.dump(person_data, file, indent=4)
            
        