from django.shortcuts import render
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from nltk.corpus import stopwords


def home(request):
    predictions = []
    data = pd.read_csv("/media/sarwechabro/Sarwech's Files/AI/machinelearning/movies.csv")
    genre = request.POST.get('genre')
    descrip = request.POST.get('desc')
    pat = r"[0-9…!?:;(',)]"
    data['Title']=data['Title'].apply(lambda x: re.sub(pat,'',x))
    data['Description']=data['Description'].apply(lambda x: re.sub(pat,'',x))
    stop_words = stopwords.words('english')
    data['Description']=data['Description'].astype(str).apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    X = data[['Genre','Description']]
    x_combined=X.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
    y= data['Title']
    tfidfvectorizer = TfidfVectorizer()
    x_tfidf = tfidfvectorizer.fit_transform(x_combined)
    x_train, x_test, y_train, y_test = train_test_split(x_tfidf,y,test_size=0.30, random_state=42)
    Gclassifier = GaussianNB()
    Gclassifier.fit(x_train.toarray(), y_train)
    if genre and descrip:
        input_vector = tfidfvectorizer.transform([genre.lower(), descrip.lower()])
        prediction = Gclassifier.predict(input_vector.toarray())
        for movies in prediction:
            if movies not in predictions:
                predictions.append(movies)
                
    
    return render(request, "machinelearning/home.html",{"prediction":predictions,})
