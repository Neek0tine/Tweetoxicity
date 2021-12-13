from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

def cleaning(text):
    stop_words = stopwords.words('english')
    lemma = WordNetLemmatizer()
    
    emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"
    
    text = text.lower()
    text = re.sub(urlPattern, ' ', text)
    text = re.sub(userPattern, ' ', text)
    text = re.sub(alphaPattern, " ", text)
    text = re.sub(sequencePattern, seqReplacePattern, text)
    for emoji in emojis.keys():
        text = text.replace(emoji, "EMOJI" + emojis[emoji])
    if len(text) > 1:
        text = ' '.join([lemma.lemmatize(word) for word in word_tokenize(text) if word not in (stop_words)])
    text = text.strip()
    
    return text

def flat(t):
    return [item for sublist in t for item in sublist]


def decode_sentiment(label):
    sentiment_map = {0: "NEGATIVE", 2: "NEUTRAL", 4: "POSITIVE"}
    return sentiment_map[int(label)]