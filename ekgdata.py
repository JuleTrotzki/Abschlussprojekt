import json
import pandas as pd
import plotly.graph_objs as go
import os
from fitparse import FitFile
import numpy as np

# %% Objekt-Welt


class EKGdata:
    """
    Klasse zum Verarbeiten und Analysieren von EKG-Daten.

    Funktionen:
    - __init__(self, ekg_dict): Konstruktor, der die EKG-Daten aus einer Datei einliest.
    - load_ekg_data(): Statische Methode zum Laden der EKG-Daten aus einer JSON-Datei.
    - load_fit_data(self, fit_file): Methode zum Laden von FIT-Dateien und Konvertierung in ein DataFrame.
    - load_by_id(test_id): Statische Methode zum Laden von EKG-Daten basierend auf der Test-ID.
    - find_peaks(series, threshold=345, respacing_factor=1): Statische Methode zum Finden der Peaks in EKG-Daten.
    - calculate_HR(peaks, sampling_rate=1000, smooth_window_size=5): Methode zur Berechnung der Herzfrequenz aus den Peaks.
    - calculate_HRV(peaks, sampling_rate=1000): Statische Methode zur Berechnung der Herzratenvariabilität (HRV) aus den Peaks.
    - plot_time_series(df, peaks, start_index=None, end_index=None): Methode zum Plotten der EKG-Zeitreihe mit Peaks.
    - plot_fit_data(df): Statische Methode zum Plotten der Herzfrequenzdaten aus einer FIT-Datei.
    """
    
    def __init__(self, ekg_dict):
        pass
        self.id = ekg_dict["id"]
        self.data = ekg_dict["result_link"]
        if self.data is None:
            raise ValueError("EKG data does not contain 'result_link'")
        
        if self.data.endswith(".csv"):
            self.df = pd.read_csv(self.data)
        elif self.data.endswith(".txt"):
            self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        elif self.data.endswith(".fit"):
            self.df = self.load_fit_data(self.data)
        else:
            raise ValueError("Unsupported file format")
        
        if 'Time in ms' in self.df.columns:
            self.df['Time in s'] = self.df['Time in ms'] / 1000
        else:
            self.df['Time in s'] = self.df.index

    
    @staticmethod  
    def load_ekg_data():
        file = open("data/ekg_data")
        ekg_data = json.load(file)
        return ekg_data
    
    
    # Funktion zum Laden von FIT Dateien
    def load_fit_data(self, fit_file):
        fit_file = FitFile(fit_file)
        records = []
        for record in fit_file.get_messages():
            record_data = {}
            for field in record:
                record_data[field.name] = field.value
            records.append(record_data)
        hr_data = pd.DataFrame(records)
        hr_data['Time in s'] = hr_data.index
        return hr_data
    
    #Erkennung an Test ID
    @staticmethod
    def load_by_id(test_id):
        with open("data/person_db.json") as file:
            person_data = json.load(file)
            for person in person_data:
                for ekg_test in person["ekg_tests"]:
                    if ekg_test["id"] == test_id:
                        if "result_link" in ekg_test:
                            return {"id": test_id, "result_link": ekg_test["result_link"]}
        
        ekg_dir = "ekg_data"
        for file_name in os.listdir(ekg_dir):
            if file_name.startswith(f"{test_id}_"):
                file_path = os.path.join(ekg_dir, file_name)
                return {"id": test_id, "result_link": file_path}
        
        print(f"Keine Datei für Test ID '{test_id}' gefunden.")
        return None
    
    

    @staticmethod  
    def find_peaks(series, threshold=345, respacing_factor=1):
   
        # Respace the series
        series = series.iloc[::respacing_factor]
     
        # Filter the series
        series = series[series>threshold]
        
        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index-respacing_factor)

        return peaks
    

    # Berechnung Herzfrequenz   
    def calculate_HR(peaks, sampling_rate=1000, smooth_window_size=5):
    
        timepoints = [peak / sampling_rate for peak in peaks[1:]]
        
        peak_intervals = pd.Series(peaks).diff().iloc[1:] / sampling_rate
        heart_rates = 60 / peak_intervals
        
        # Glättung der Herzfrequenzdaten durch Moving Average
        smoothed_heart_rates = heart_rates.rolling(window=smooth_window_size, min_periods=1).mean()
    
        df = pd.DataFrame({'Zeitpunkt': timepoints, 'Herzfrequenz': smoothed_heart_rates})
       

        return df
    
    
    #Berechnung Herzratenvariabilität
    @staticmethod
    def calculate_HRV(peaks, sampling_rate=1000):
        peak_intervals = np.diff(peaks) / sampling_rate
        sdnn = np.std(peak_intervals)
        rmssd = np.sqrt(np.mean(np.square(np.diff(peak_intervals))))
        nn50 = np.sum(np.abs(np.diff(peak_intervals)) > 0.05)
        pnn50 = nn50 / len(peak_intervals) * 100

        hrv_metrics = {
            'SDNN': sdnn,
            'RMSSD': rmssd,
            'NN50': nn50,
            'PNN50': pnn50
        }
        return hrv_metrics
    
        
    #Plot EKG-Daten
    def plot_time_series(df, peaks, start_index=None, end_index=None):
        
        if start_index is None:
            start_index = 0
        if end_index is None:
            end_index = len(df)
        
    
        df = df.iloc[start_index:end_index]
        
        peaks_in_range = [peak for peak in peaks if start_index <= peak < end_index]
        peak_times = df.iloc[peaks_in_range]['Time in s']
        peak_values = df.iloc[peaks_in_range]['EKG in mV']
        
        fig = go.Figure()

        # EKG-Daten plotten
        fig.add_trace(go.Scatter(
            x=df['Time in s'], 
            y=df['EKG in mV'],
            mode='lines',
            name='EKG Data'))

        # Peaks hinzufügen
        fig.add_trace(go.Scatter(
            x=peak_times,
            y=peak_values,
            mode='markers',
            marker=dict(color='red', size=5),
            name='Peaks'))

        # Layout anpassen
        fig.update_layout(
            title='EKG Daten',
            xaxis_title='Time in s',
            yaxis_title='EKG in mV',
            showlegend=True)

        
        return fig

    #Plot Herzfrequez aus fit Datei
    @staticmethod
    def plot_fit_data(df):
        fig = go.Figure()

        # Herzfrequenz über Zeit plotten, falls vorhanden
        if 'heart_rate' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Time in s'],
                y=df['heart_rate'],
                mode='lines',
                name='Herzfrequenz'))
            
            # Layout anpassen
            fig.update_layout(
                title='Herzfrequenz',
                xaxis_title='Zeit',
                yaxis_title='Herzfrequenz (Schläge / min)')
        
        return fig
    
    