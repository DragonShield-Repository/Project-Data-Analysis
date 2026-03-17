Der Code wurde Schrittweise geschrieben.
Jeder weitere Schritt enthält auch den Code der vorherigen Schritte.
Kommentare zum Code sind nur in seinem jeweiligen zugehörigen Schritt ausfürhlich vorhanden:

1. comcast_consumeraffairs_complaints.csv: unbearbeitete Datei, welche mehrere Kundenbeschwerden enthält 
2. text_einlesen: Die csv Datei wird mittels Pandas eingelesen
3. text_bereinigen: Der Text in der csv wird von Sonderzeichen, Satzzeichen und überflüssigen Leerzeichen befreit, sowie in Kleinbuchstaben umgewandelt
4. text_rechtschreibung: Der Text wird von Rechtschreibfehlern befreit
5. text_tokenisieren: Der Text wird tokenisiert
6. text_lemmatisierung: Die Wörter im Text werden in ihre Grundform umgewandelt
7. text_stopwords_FINALERCODE: Der Text wird von allen Stopwörtern befreit
8. comcast_tokens_final.csv: Enthält den Text nach all seinen Bearbeitungsschritten und wird für die weiteren Schritte verwendet
