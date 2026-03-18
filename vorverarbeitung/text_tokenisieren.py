import pandas as pd
import re
from tqdm import tqdm
from spellchecker import SpellChecker
import nltk
from nltk.tokenize import word_tokenize

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
spell = SpellChecker(distance=1)  

whitelist = {'comcast', 'xfinity', 'wow'}

custom_words = {
    'ive': 'i have',
    'dont': 'do not',
    'cant': 'cannot',
    'wont': 'will not'
}

def korrigiere_text(text):
    words = text.split()
    corrected_words = []
    for w in words:
        if w in whitelist:
            corrected_words.append(w)  
        elif w in custom_words:  
            corrected_words.append(custom_words[w])
        else:
            corrected_words.append(spell.correction(w) or w)
    return ' '.join(corrected_words)

df['text_korrigiert'] = df['text_bereinigt'].progress_apply(korrigiere_text)

# 4. Tokenisierung der csv
df['tokens'] = df['text_korrigiert'].progress_apply(word_tokenize)  # Anwendung der Funktion word_tokenize inkl. Fortschrittsbalken

print(df[['text_korrigiert', 'tokens']].head())   # Erste 5 Zeilen des Ergebnisses 
