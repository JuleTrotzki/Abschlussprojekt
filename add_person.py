import os
import json
from datetime import datetime
import streamlit as st

def add_person(get_text):
    """
    Diese Funktion ermöglicht es, eine neue Person mit den entsprechenden Daten
    hinzuzufügen, einschließlich des Hochladens eines Bildes und EKG-Daten.
    """

    # Setzt den Header der Seite auf "Neue Person anlegen" basierend auf der ausgewählten Sprache
    st.header(get_text({"Deutsch": "Neue Person anlegen", "English": "Add New Person"}))

    # Eingabefelder für Vorname, Nachname und Geburtsjahr
    firstname = st.text_input(get_text({"Deutsch": "Vorname", "English": "First Name"}))
    lastname = st.text_input(get_text({"Deutsch": "Nachname", "English": "Last Name"}))
    birth_year = st.number_input(get_text({"Deutsch": "Geburtsjahr", "English": "Birth Year"}), min_value=1900, max_value=2100, value=2000, step=1)
    
    # Felder zum Hochladen von Bildern und EKG-Daten
    picture_path = st.file_uploader(get_text({"Deutsch": "Bild hochladen", "English": "Upload Picture"}), type=["jpg", "jpeg", "png"])
    ekg_file = st.file_uploader(get_text({"Deutsch": "EKG-Daten hochladen", "English": "Upload EKG Data"}), type=["csv", "txt", "fit"])

    # Button zum Speichern der Personendaten
    if st.button(get_text({"Deutsch": "Person speichern", "English": "Save Person"})):
        # Überprüfung, ob alle erforderlichen Felder ausgefüllt sind
        if not firstname or not lastname or not birth_year:
            st.error(get_text({"Deutsch": "Bitte füllen Sie alle Felder aus!", "English": "Please fill out all fields!"}))
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

        st.success(get_text({"Deutsch": "Person erfolgreich angelegt!", "English": "Person successfully added!"}))

        # Speichern der EKG-Daten (falls hochgeladen)
        if ekg_file:
            ekg_dir = "ekg_data"
            os.makedirs(ekg_dir, exist_ok=True)
            ekg_path_save = os.path.join(ekg_dir, f"{ekg_file.name}")
            with open(ekg_path_save, "wb") as f:
                f.write(ekg_file.getbuffer())

            # Hinzufügen des EKG-Datensatzes zur Person
            for person in person_data:
                if person["id"] == new_id:
                    person["ekg_tests"].append({
                        "id": new_id,
                        "date": datetime.now().strftime('%d.%m.%Y'),
                        "result_link": ekg_path_save})
            with open("data/person_db.json", "w") as file:
                json.dump(person_data, file, indent=4)

if __name__ == "__main__":
    add_person(lambda x: x['English'])  # Beispiel für die Standard-Sprache
