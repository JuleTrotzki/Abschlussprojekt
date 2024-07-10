# Beat Analyzer

## Übersicht

Diese BeatAnalyzer-App ermöglicht es Benutzern, EKG-Daten von verschiedenen Personen zu analysieren. Die App bietet Funktionen zum Anzeigen von Personendaten, zum Auswählen und Visualisieren von EKG-Tests, zur Erkennung von Peaks in den EKG-Daten und zur Berechnung der Herzfrequenz sowie der Herzratenvariabilität.

## Funktionen

- **Login**: Authentifizierung der Benutzer.
- **Personenauswahl**: Auswahl einer Person aus einer Liste und Anzeige ihrer Informationen.
- **EKG-Datenanzeige**: Visualisierung der EKG-Daten und Berechnung der Herzratenvariabilität (HRV).
- **Mehrsprachige Unterstützung**: Benutzeroberfläche in Deutsch und Englisch.

## Installationsanleitung

1. **Klone das Repository:**
    git clone https://github.com/JuleTrotzki/Abschlussprojekt

2. **Erstelle ein virtuelles Environment und installiere die Abhängigkeiten:**
    python -m venv .venv
    .venv\Scripts\activate

    Installiere die erforderlichen Abhängigkeiten:
    pip install -r requirements.txt

## Verwendung
Öffne eine Befehlszeile, navigiere zum Projektordner und führe den folgenden Befehl aus, um das Programm auszuführen:

streamlit run main.py

Sie sehen nun die Homepage mit Informationen über die App. In der Menü-Leiste links können sie zum Login navigieren und sich mit Ihrem Benutzernamen und einem Passwort einloggen. Nun können sie unter EKG-Daten die Daten der verschiedenen Personen einsehen und eine neue Person und anlegen. 

