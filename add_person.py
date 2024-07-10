import os
import json
from datetime import datetime
import streamlit as st
from tinydb import TinyDB, Query
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker

# SQLite setup
DATABASE_URL = "sqlite:///person_db.sqlite"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

persons_table = Table(
    'persons', metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String),
    Column('lastname', String),
    Column('date_of_birth', String),
    Column('picture_path', String),
)

ekg_tests_table = Table(
    'ekg_tests', metadata,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer),
    Column('date', String),
    Column('result_link', String),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_person(get_text):
    """
    Diese Funktion ermöglicht es, eine neue Person mit den entsprechenden Daten
    hinzuzufügen, einschließlich des Hochladens eines Bildes und EKG-Daten.
    """

    st.header(get_text({"Deutsch": "Neue Person anlegen", "English": "Add New Person"}))

    firstname = st.text_input(get_text({"Deutsch": "Vorname", "English": "First Name"}))
    lastname = st.text_input(get_text({"Deutsch": "Nachname", "English": "Last Name"}))
    birth_year = st.number_input(get_text({"Deutsch": "Geburtsjahr", "English": "Birth Year"}), min_value=1900, max_value=2100, value=2000, step=1)

    picture_path = st.file_uploader(get_text({"Deutsch": "Bild hochladen", "English": "Upload Picture"}), type=["jpg", "jpeg", "png"])
    ekg_file = st.file_uploader(get_text({"Deutsch": "EKG-Daten hochladen", "English": "Upload EKG Data"}), type=["csv", "txt", "fit"])

    if st.button(get_text({"Deutsch": "Person speichern", "English": "Save Person"})):
        if not firstname or not lastname or not birth_year:
            st.error(get_text({"Deutsch": "Bitte füllen Sie alle Felder aus!", "English": "Please fill out all fields!"}))
            return

        if picture_path:
            picture_dir = "uploaded_pictures"
            os.makedirs(picture_dir, exist_ok=True)
            picture_path_save = os.path.join(picture_dir, picture_path.name)
            with open(picture_path_save, "wb") as f:
                f.write(picture_path.getbuffer())
        else:
            picture_path_save = ""

        try:
            with open("data/person_db.json", "r") as file:
                person_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            person_data = []

        new_id = max([person["id"] for person in person_data], default=0) + 1

        new_person = {
            "id": new_id,
            "firstname": firstname,
            "lastname": lastname,
            "date_of_birth": str(birth_year),
            "picture_path": picture_path_save,
            "ekg_tests": []
        }
        person_data.append(new_person)

        with open("data/person_db.json", "w") as file:
            json.dump(person_data, file, indent=4)

        st.success(get_text({"Deutsch": "Person erfolgreich angelegt!", "English": "Person successfully added!"}))

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

        # TinyDB
        db = TinyDB("data/tiny_person_db.json")
        db.insert(new_person)

        # SQL
        new_person_sql = persons_table.insert().values(
            id=new_id,
            firstname=firstname,
            lastname=lastname,
            date_of_birth=str(birth_year),
            picture_path=picture_path_save
        )
        session.execute(new_person_sql)
        session.commit()

        if ekg_file:
            new_ekg_test_sql = ekg_tests_table.insert().values(
                person_id=new_id,
                date=datetime.now().strftime('%d.%m.%Y'),
                result_link=ekg_path_save
            )
            session.execute(new_ekg_test_sql)
            session.commit()

if __name__ == "__main__":
    add_person(lambda x: x['English'])  # Beispiel für die Standard-Sprache
