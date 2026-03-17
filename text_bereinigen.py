import pandas as pd
import re

# 1. csv-Datei wird eingelesen 
csv_path = "comcast_daten/comcast_consumeraffairs_complaints.csv"
df = pd.read_csv(csv_path, header=None, skiprows=1)     

df.columns = ['author', 'posted_on', 'rating', 'text']

# 2. Texte bereinigen (Zahlen & Sonderzeichen entfernen)
def bereinige_text(text):                        # definieren einer neuen Funktion
    if pd.isnull(text):                          # prüfen, ob es sich um einen leeren Wert handelt
        return ""
    text = str(text)                             # sicherstellen, dass es ein String ist
    text = text.lower()                          # Umwandlung in Kleinbuchstaben
    text = re.sub(r'[^a-zA-Z\s]', '', text)      # nur Buchstaben & Leerzeichen behalten
    text = re.sub(r'\s+', ' ', text)             # mehrere Leerzeichen auf eins reduzieren
    return text.strip()                          # Entfernen der Leerzeichen am Anfang/ Ende eines Textes

df['text_bereinigt'] = df['text'].apply(bereinige_text)   # Anwendung der definierten Funktion auf Spalte

print(df[['text', 'text_bereinigt']].head())   # Erste 5 Zeilen des Ergebnisses 