import pandas as pd
import numpy as np
import pickle
import nltk
import re
import os
import emoji
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


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

    with open('scripts/pickle/CombineModel.pkl', 'rb') as file:
        model = pickle.load(file)

    # Import Vecorizer (text token)
    with open('scripts/pickle/vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)

    return model, vectorizer


def predict(model, vectorizer, texts):
    print('===DEBUG PREDICT===')
    data = []

    for index, text in enumerate(texts):
        print(f'\r [+] Predicting tweets {index + 1} of {len(texts)}', end='')
        # Text Cleaning (scripts ada di packages/text/__init__.py)
        txt = emoji.demojize(text, delimiters=("", " "))
        clean = cleaning(txt)
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
    print()
    df = pd.DataFrame(data, columns=['original text', 'clean text', 'sentiment', 'confidence'])
    
    df.dropna(inplace=True)
    
    print('===DEBUG LOAD MODEL END===')
    return df


def account_sentiment(df):
    print('===DEBUG ACCOUNT SENTIMENT START===')

    df_count_sentiment = df['sentiment'].value_counts().to_frame()
    
    df_count = []
    if (list(df_count_sentiment.index) == ['POSITIVE', 'NEGATIVE']) or (list(df_count_sentiment.index) == ['NEGATIVE', 'POSITIVE']):
        df_count = df_count_sentiment
    elif list(df_count_sentiment.index) == ['POSITIVE']:
        df_count_sentiment.loc['NEGATIVE'] = 0
        df_count = df_count_sentiment
    elif list(df_count_sentiment.index) == ['NEGATIVE']:
        df_count_sentiment.loc['POSITIVE'] = 0
        df_count = df_count_sentiment

    df_count['percentage'] = round(
        df_count['sentiment'] / df_count['sentiment'].sum() * 100, 2)

    df_count = df_count.reset_index().rename({'index': 'final_sentiment'}, axis=1)

    sentiment_max = df_count.loc[df_count['sentiment'] == (df_count['sentiment'].max()), 'final_sentiment'].iloc[0]

    print('===DEBUG ACCOUNT SENTIMENT END===')
    return sentiment_max, df_count


def models_script(datas):
    
    # read user inputs
    data = datas['Text']
    
    # Inisiasi Pickle File
    model, vetorizer = load_model()

    # inisiasi predict
    models = predict(model, vetorizer, data)
    print(models)

    sentiment_final, sentiment_count = account_sentiment(models)

    return models, sentiment_final, sentiment_count


# def UnitTesting():
#     _query = pd.DataFrame({
#         'Text':['Hello my name is fathur']
#     })
    
#     return models_script(_query)

# UnitTesting()