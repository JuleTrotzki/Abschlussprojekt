import json
import pandas as pd
import plotly.graph_objs as go



# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
    
    @staticmethod  
    def load_ekg_data():
        file = open("data/ekg_data")
        ekg_data = json.load(file)
        return ekg_data
    
    def load_by_id(test_id):
        with open("data/person_db.json") as file:
            ekg_data = json.load(file)
            for person in ekg_data:
                for ekg_test in person["ekg_tests"]:
                    if ekg_test["id"] == test_id:
                        return ekg_test
        return {}


    @staticmethod  
    def find_peaks(series, threshold, respacing_factor=5):
   
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
    
   # def calculate_HR(peaks, respacing_factor=5, sampling_rate=1000):
    #    peak_intervals = pd.Series(peaks).diff()
        #peak_intervals_seconds = peak_intervals / (sampling_rate / respacing_factor) #in sekunden
     #   heart_rates = 60 / peak_intervals
      #  heart_rates = heart_rates.dropna()*2
    
       # df = pd.DataFrame({'Zeitpunkt': peaks[1:], 'Herzfrequenz': heart_rates})
    
        #return df
        
    def calculate_HR(peaks, sampling_rate=1000, smooth_window_size=3):
    
        peak_intervals = pd.Series(peaks).diff().iloc[1:] / sampling_rate
        heart_rates = 60 / peak_intervals
        
        # Glättung der Herzfrequenzdaten durch Moving Average
        smoothed_heart_rates = heart_rates.rolling(window=smooth_window_size, min_periods=1).mean()
    
        timepoints = peaks[1:]
    
        df = pd.DataFrame({'Zeitpunkt': timepoints, 'Herzfrequenz': smoothed_heart_rates})
        
        return df
    
    

    def plot_time_series(df, peaks, start_index=None, end_index=None):
        
        if start_index is None:
            start_index = 0
        if end_index is None:
            end_index = len(df)
        
    
        df = df.iloc[start_index:end_index]
        
        peaks_in_range = [peak for peak in peaks if start_index <= peak < end_index]
        peak_times = df.iloc[peaks_in_range]['Time in ms']
        peak_values = df.iloc[peaks_in_range]['EKG in mV']
        
        fig = go.Figure()

        # EKG-Daten plotten
        fig.add_trace(go.Scatter(
            x=df['Time in ms'], 
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
            title='EKG Data',
            xaxis_title='Time in ms',
            yaxis_title='EKG in mV',
            showlegend=True)

        return fig
    
if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    
    # Beispielaufruf der Methode load_by_id
    test_id = 1
    ekg_test_data = EKGdata.load_by_id(test_id)

    if ekg_test_data:
        print("Gefundene EKG-Testdaten:")
        print(ekg_test_data)
    else:
        print("EKG-Test mit der angegebenen ID wurde nicht gefunden.")
        
    # Beispielaufruf find_peaks
    file_path = "data/ekg_data/01_Ruhe.txt"
    ekg_data = pd.read_csv(file_path, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
    threshold = 345
    peaks = EKGdata.find_peaks(ekg_data['EKG in mV'], threshold)
    print("Gefundene Peaks:", peaks)
    fig = EKGdata.plot_time_series(ekg_data, peaks)
    fig.show()
    
    # Beispielaufruf estimate_HR
    heart_rate = EKGdata.calculate_HR(peaks)
    print("Geschätzte Herzfrequenz:", heart_rate, "Schläge pro Minute")
    
    

    