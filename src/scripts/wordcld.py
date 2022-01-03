from numpy import NaN
from wordcloud import WordCloud
from PIL import Image
import pandas as pd

def readCSV():
    path = r'C:\Users\fathu\Downloads\data (17).csv'
    df = pd.read_csv(path)
    df.replace("", NaN, inplace=True)
    df.dropna(inplace=True)
    return df

def WORDCLOUD(df):
    file = " ".join(str(v) for v in df['clean text'])
    
    WC = WordCloud(
        max_words=len(df),
        width=810,
        height=500,
        background_color="white"
    ).generate(file)
    
    return WC.to_file('scripts/static/bootstrap/img/wordcloud.png')

    

    
    
    