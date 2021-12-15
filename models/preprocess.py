# util
import pandas as pd

# text cleaning
from packages.text import cleaning, decode_sentiment

def load_data():
    path = "./data/twitter_sentiment.csv"
    column_names = ["target", "id", "date", "flag", "user", "text"]
    chunks = pd.read_csv(path, chunksize=100000, encoding='ISO-8859-1', names=column_names)
    concat_df = pd.concat(chunks).sample(frac=1, random_state=42).reset_index(drop=True)
    
    df = concat_df.drop(columns=["id", "date", "flag", "user"])
    
    df['target'] = df['target'].apply(lambda x: decode_sentiment(x))
    
    return text_cleaning(df)
    
def text_cleaning(df):
    df['cleaned_text'] = df['text'].apply(lambda x: cleaning(x))
    print(df.head())
    
    return exportCSV(df)
    
def exportCSV(df):
    df.to_csv('clean_twitter_sentimen.csv', index=False)
    

def main():
    load_data()
    

if __name__ == '__main__':
    main()