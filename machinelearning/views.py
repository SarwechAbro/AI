from django.shortcuts import render
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB

def home(request):
    predictions = []
    data = pd.read_csv("/home/sarwechabro/Python Work/movies.csv")
    genre = request.POST.get('genre').lower()
    descrip = request.POST.get('desc').lower()
    pat = r'[0-9…!؟:;("،)]'
    data['Title']=data['Title'].apply(lambda x: re.sub(pat,'',x))
    tfidfvectorizer = TfidfVectorizer()
    X = data[['Genre','Description']]
    x_combined=X.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
    x_tfidf = tfidfvectorizer.fit_transform(x_combined)
    y= data['Title']
    x_train, x_test, y_train, y_test = train_test_split(x_tfidf,y,test_size=0.30, random_state=42)
    Gclassifier = GaussianNB()
    Gclassifier.fit(x_train.toarray(), y_train)
    if genre and descrip:
        input_vector = tfidfvectorizer.transform([genre, descrip])
        prediction = Gclassifier.predict(input_vector.toarray())
        for movies in prediction:
            if movies not in predictions:
                predictions.append(movies)
                
    
    return render(request, "machinelearning/home.html",{"prediction":predictions,})
