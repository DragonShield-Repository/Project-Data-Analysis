import pandas as pd
import re
from tqdm import tqdm
from spellchecker import SpellChecker


# Fortschrittsbalken für pandas apply aktivieren
tqdm.pandas()

# 1. CSV-Datei einlesen
csv_path = "comcast_daten/comcast_consumeraffairs_complaints.csv"
df = pd.read_csv(csv_path, header=None, skiprows=1)

df.columns = ['author', 'posted_on', 'rating', 'text']

# 2. Texte bereinigen (Zahlen & Sonderzeichen entfernen)
def bereinige_text(text):
    if pd.isnull(text):
        return ""
    text = str(text)  
    text = text.lower() 
    text = re.sub(r'[^a-zA-Z\s]', '', text)  
    text = re.sub(r'\s+', ' ', text)          
    return text.strip()

df['text_bereinigt'] = df['text'].apply(bereinige_text)

# 3. Rechtschreibung korrigieren mit pyspellchecker
spell = SpellChecker(distance=1)             # kleinere Tippfehler mit distance=1 adressieren, sodass die Abweichung nicht zu groß wird

whitelist = {'comcast', 'xfinity', 'wow'}    # Wörter, die nicht verändert werden sollen

custom_words = {                               # Kurzformen in das eigentliche Wort umwandeln
    'ive': 'i have',
    'dont': 'do not',
    'cant': 'cannot',
    'wont': 'will not'
}

def korrigiere_text_safe(text):                     # definieren einer neuen Funktion
    words = text.split()                            # Der Text wird anhand der Leerzeichen getrennt
    corrected_words = []                            # neues Array für die korrigierten Wörter
    for w in words:                                 # Jedes Wort wird separat betrachtet
        if w in whitelist:                          # Wörter innerhalb der Whitelist werden nicht verändert
            corrected_words.append(w)  
        elif w in custom_words:                     # Wörter, die in custom_words definiert wurden, werden entsprechend umgewandelt
            corrected_words.append(custom_words[w])
        else:
            corrected_words.append(spell.correction(w) or w)  # Wenn weder Whitelist noch custom_words: Wort wird korrigiert
    return ' '.join(corrected_words)                # Die Liste korrigierter Wörter wird wieder zusammengeführt

df['text_korrigiert'] = df['text_bereinigt'].progress_apply(korrigiere_text_safe)  # Anwendung definierter Funktion auf vorherig erstellte Spalte inkl. Fortschrittsbalken

print(df[['text_bereinigt', 'text_korrigiert']].head())   # Erste 5 Zeilen des Ergebnisses 

