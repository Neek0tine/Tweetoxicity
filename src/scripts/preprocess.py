import pickle
import numpy as np
import pandas as pd
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')


def cleaning(text):
    stop_words = stopwords.words('english')
    lemma = WordNetLemmatizer()

    emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
              ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
              ':-@': 'shocked', ':@': 'shocked', ':-$': 'confused', ':\\': 'annoyed',
              ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
              '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
              '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
              ';-)': 'wink', 'O:-)': 'angel', 'O*-)': 'angel', '(:-D': 'gossip', '=^.^=': 'cat'}

    urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern = '@[^\s]+'
    alphaPattern = "[^a-zA-Z0-9]"
    sequencePattern = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"

    text = text.lower()
    text = re.sub(urlPattern, ' ', text)
    text = re.sub(userPattern, ' ', text)
    text = re.sub(alphaPattern, " ", text)
    text = re.sub(sequencePattern, seqReplacePattern, text)
    for emoji in emojis.keys():
        text = text.replace(emoji, "EMOJI" + emojis[emoji])
    if len(text) > 1:
        text = ' '.join([lemma.lemmatize(word) for word in word_tokenize(text) if word not in stop_words])
    text = text.strip()

    return text


def flat(text):
    return [item for sublist in text for item in sublist]


def load_model():
    print('===DEBUG LOAD MODEL===')
    # Import Model

    with open('pickle/CombineModel.pkl', 'rb') as file:
        model = pickle.load(file)

    # Import Vecorizer (text token)
    with open('pickle/vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)

    return model, vectorizer


def predict(model, vectorizer, texts):
    print('===DEBUG PREDICT===')
    data = []

    for text in texts:
        # Text Cleaning (scripts ada di packages/text/__init__.py)
        clean = cleaning(text)
        # vectorization
        vec_inputs = vectorizer.transform([clean])

        # return sentiment (NEGATIVE or POSITIVE)
        LRpred = model['LRmodel'].predict(vec_inputs)
        SVCpred = model['SVCmodel'].predict(vec_inputs)
        BNBpred = model['BNBmodel'].predict(vec_inputs)

        # return confidence score (0 - 1)
        LRpred_conf = max(flat(model['LRmodel'].predict_proba(vec_inputs)))
        SVCpred_conf = max(flat(model['SVCmodel'].predict_proba(vec_inputs)))
        BNBpred_conf = max(flat(model['BNBmodel'].predict_proba(vec_inputs)))

        result = np.concatenate((LRpred, SVCpred, BNBpred))
        result_conf = [LRpred_conf, SVCpred_conf, BNBpred_conf]

        result = pd.DataFrame({
            'model': ['Logistic Reg', 'SVM', 'NB'],
            'predict': result,
            'confidence': result_conf
        })

        # majority model algorithm
        result_pred = result.predict.mode()[0]
        confidence = f"{round(result[result['predict'] == result.predict.mode()[0]]['confidence'].mean() * 100, 2)}%"

        data.append((text, clean, result_pred, confidence))

    df = pd.DataFrame(data, columns=['original text', 'clean text', 'sentiment', 'confidence'])
    print('===DEBUG LOAD MODEL END===')
    return df


def account_sentiment(df):
    print('===DEBUG ACCOUNT SENTIMENT START===')

    df_count_sentiment = df['sentiment'].value_counts().to_frame()
    df_count_sentiment['percentage'] = round(
        df_count_sentiment['sentiment'] / df_count_sentiment['sentiment'].sum() * 100, 2)
    df_count_sentiment = df_count_sentiment.reset_index().rename({'index': 'final_sentiment'}, axis=1)

    sentiment_max = df_count_sentiment['final_sentiment'].max()
    print('===DEBUG ACCOUNT SENTIMENT END===')
    return sentiment_max


def models_script(datas):
    # read user inputs
    data = datas['Text']
    # Inisiasi Pickle File
    model, vetorizer = load_model()

    # inisiasi predict
    models = predict(model, vetorizer, data)

    sentiment = account_sentiment(models)

    return models, sentiment
