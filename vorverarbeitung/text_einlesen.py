import pandas as pd

# Pfad zur CSV-Datei
csv_path = "comcast_daten/comcast_consumeraffairs_complaints.csv"  

# CSV einlesen, erste Zeile wird aufgrund des Headers übersprungen
df = pd.read_csv(csv_path, header=None, skiprows=1)  # DataFrame wird in der Variable df gespeichert

# Spalten benennen, entsprechend des Headers
df.columns = ['author', 'posted_on', 'rating', 'text']

# Erste 5 Zeilen anzeigen
print("Erste 5 Zeilen des Datensatzes:")
print(df.head())
