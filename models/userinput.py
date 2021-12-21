import pickle
import numpy as np
import pandas as pd
from packages.text import cleaning, flat


def load_model():
    # Import Model
    file = open('./pickle/CombineModel.pkl', 'rb')
    model = pickle.load(file)
    file.close()

    # Import Vecorizer (text token)
    file = open('./pickle/vectorizer.pkl', 'rb')
    vectorizer = pickle.load(file)
    file.close
    
    return model, vectorizer

def predict(model, vectorizer, texts):
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
        confidence = round(result[result['predict'] == result.predict.mode()[0]]['confidence'].mean()*100,2)
        
        data.append((text, clean, result_pred, confidence))
        
    df = pd.DataFrame(data, columns=['original text', 'clean text','sentiment', 'confidence'])
    print(df.head())
    
    return df

def SaveCSV(data):
    export = data.to_csv('text.csv', index=False)

def ratio(df):
    POSITIVE = df['sentiment'].value_counts()["POSITIVE"] / len(df['sentiment']) * 100
    NEGATIVE = df['sentiment'].value_counts()["NEGATIVE"] / len(df['sentiment']) * 100

    sent_ratio = {
        'Sentiment': ["POSITIVE", "NEGATIVE"],
        'Ratio': [POSITIVE, NEGATIVE]
    }

    Result = pd.DataFrame(sent_ratio)
    print(Result)
    
    return Result


def tweetoxicity(path):
    # read user inputs
    read_text = pd.read_csv(path)
    read_text = read_text['1']
    
    # Inisiasi Pickle File
    model, vetorizer = load_model()
    
    # inisiasi predict
    models = predict(model, vetorizer, read_text)
    
    exportCSV = SaveCSV(models)
    
    sentiment_ratio = ratio(models)
    
    return models, exportCSV

if __name__ == '__main__':
    filepath = './data/Tweets of elonmusk.csv'
    AccountSentiment = tweetoxicity(filepath)
