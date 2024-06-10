from fitparse import FitFile
import pandas as pd

def read_fit_file(file_path):
    """
    Liest Daten aus einer .fit-Datei und gibt sie als Pandas DataFrame zurück.
    Parameter:
    file_path (str): Pfad zur .fit-Datei.
    Rückgabewert:
    pd.DataFrame: DataFrame mit den extrahierten Daten aus der .fit-Datei.
    """
    
    # Einlesen der .fit-Datei
    fitfile = FitFile(file_path)

    # Initialisieren einer Liste für die Datenspeicherung
    records = []

    # Durchlaufen aller 'record'-Nachrichten in der .fit-Datei
    for record in fitfile.get_messages('record'):
        data = {}
        # Extrahieren der Felder und Werte in jeder Nachricht
        for field in record:
            data[field.name] = field.value
        # Hinzufügen des extrahierten Datensatzes zur Liste
        records.append(data)

    # Umwandeln der Liste in einen Pandas DataFrame
    df = pd.DataFrame(records)
    return df

# Pfad zur .fit-Datei
file_path = 'data/long_endurance_ride.fit'

# Aufrufen der Funktion und Speichern des DataFrames
df = read_fit_file(file_path)

# Ausgabe der ersten Zeilen des DataFrames
print(df.head())