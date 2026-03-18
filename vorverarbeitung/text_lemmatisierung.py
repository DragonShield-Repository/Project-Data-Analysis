import pandas as pd
import re
from tqdm import tqdm
from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import spacy


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

df['text_korrigiert'] = df['text_bereinigt'].apply(korrigiere_text)

# 4. Tokenisierung der csv
df['tokens'] = df['text_korrigiert'].apply(word_tokenize)

# 5. Lemmatisierung der tokens
nlp = spacy.load("en_core_web_sm")  #Lädt das englische Sprachmodell

def lemmatize_tokens(tokens):  #Definieren einer neuen Funktion
    doc = nlp(" ".join(tokens))  #Für höhere Geschwindigkeit wird der Text für die Lemmatisierung wieder zusammengeführt
    return [token.lemma_ for token in doc]  #Wandelt jedes Wort in seine Grundform um

df['tokens_lemmatized'] = df['tokens'].progress_apply(lemmatize_tokens)  # Anwendung der Funktion inkl. Fortschrittsbalken

print(df[['tokens', 'tokens_lemmatized']].head())   # Erste 5 Zeilen des Ergebnisses 
