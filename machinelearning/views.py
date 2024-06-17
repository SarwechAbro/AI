from django.shortcuts import render
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB

def home(request):
    predictions = []
    data = pd.read_csv("/home/sarwechabro/movies.csv")
    genere = request.POST.get('genere')
    hero = request.POST.get('hero')
    duraion = request.POST.get('duration')
    pat = r'[0-9…!؟:;("،)]'
    data['geners']=data['geners'].apply(lambda x: re.sub(pat,'',x))
    tfidfvectorizer = TfidfVectorizer()
    X = data[['geners','hero','duration']]
    x_combined=X.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
    x_tfidf = tfidfvectorizer.fit_transform(x_combined)
    y= data['movies']
    x_train, x_test, y_train, y_test = train_test_split(x_tfidf,y,test_size=0.30, random_state=42)
    Gclassifier = GaussianNB()
    Gclassifier.fit(x_train.toarray(), y_train)
    if genere and hero and duraion:
        input_vector = tfidfvectorizer.transform([genere, hero, duraion])
        prediction = Gclassifier.predict(input_vector.toarray())
        for movies in prediction:
            if movies not in predictions:
                predictions.append(movies)
                
    
    return render(request, "machinelearning/home.html",{"prediction":predictions,})
