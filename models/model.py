# util
import pandas as pd
import pickle

# sklearn
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

def load_clean_data():
    path = "clean_twitter_sentimen.csv" 
    chunks = pd.read_csv(path, chunksize=100000, encoding='ISO-8859-1')
    df = pd.concat(chunks).sample(frac=1, random_state=42).reset_index(drop=True).dropna()
    print(df.head())
    
    return split_train_test(df)
    
def split_train_test(df):
    x = df['cleaned_text']
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=42)
    
    return vectorization(X_train, X_test, y_train, y_test)
    
def vectorization(X_train, X_test, y_train, y_test):
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=500000)
    vectorizer.fit_transform(X_train)
    
    # Pickle Vectorizer
    file = open('vectorizer.pkl', 'wb')
    pickle.dump(vectorizer, file)
    file.close()
    
    train_x_vector = vectorizer.transform(X_train)
    test_x_vector =  vectorizer.transform(X_test)
    
    return modelling(train_x_vector, test_x_vector, y_train, y_test)

def model_Evaluate(model, name, test_x_vector, y_test):
    
    # Predict values for Test dataset
    print(f'==={name}===')
    y_pred = model.predict(test_x_vector)

    # Print the evaluation metrics for the dataset.
    print(classification_report(y_test, y_pred))
    
    # Compute and plot the Confusion matrix
    cf_matrix = confusion_matrix(y_test, y_pred)
    print('\n')
    
def modelling(train_x_vector, test_x_vector, y_train, y_test):
    # Naive Bayes
    BNBmodel = BernoulliNB()
    BNBmodel.fit(train_x_vector, y_train)
    model_Evaluate(BNBmodel, "Naive Bayes", test_x_vector, y_test)
    
    # SVM Linear
    SVCmodel = LinearSVC()
    SVCmodel = CalibratedClassifierCV(SVCmodel)
    SVCmodel.fit(train_x_vector, y_train)
    model_Evaluate(SVCmodel, "SVM", test_x_vector, y_test)
    
    # Logistic Regression
    LRmodel = LogisticRegression(max_iter=1000)
    LRmodel.fit(train_x_vector, y_train)
    model_Evaluate(LRmodel, "Logistic Regression", test_x_vector, y_test)
    
    return saving_files(BNBmodel, SVCmodel, LRmodel)
    
def saving_files(BNBmodel, SVCmodel, LRmodel):  
    # Model
    
    models = {
        "LRmodel": BNBmodel,
        "SVCmodel": SVCmodel,
        "BNBmodel": LRmodel
    }
    
    file =  open('CombineModel.pkl', 'wb')
    pickle.dump(models, file)
    file.close()

        
def main():
    load_clean_data()
    

if __name__ == '__main__':
    main()
    