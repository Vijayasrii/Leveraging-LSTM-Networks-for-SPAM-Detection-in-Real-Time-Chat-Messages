import os
import re
import string
import pandas as pd
import nltk

from django.shortcuts import render
from django.conf import settings

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# Download nltk resources
nltk.download('stopwords')

from nltk.corpus import stopwords
stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))

# =========================
# Load Dataset
# =========================

path1 = os.path.join(settings.MEDIA_ROOT, 'labeled_data.csv')
df_offensive = pd.read_csv(path1, nrows=500)

df_offensive.drop(['Unnamed: 0','count','hate_speech','offensive_language','neither'],axis=1,inplace=True)

# =========================
# Text Cleaning Function
# =========================

def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)

    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)

    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)

    return text

df_offensive['tweet'] = df_offensive['tweet'].apply(clean_text)

# =========================
# Train Test Split
# =========================

x = df_offensive['tweet']
y = df_offensive['class']

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)

# =========================
# Vectorization
# =========================

count = CountVectorizer(stop_words='english')
x_train_vectorizer = count.fit_transform(x_train)
x_test_vectorizer = count.transform(x_test)

tfidf = TfidfTransformer()

x_train_tfidf = tfidf.fit_transform(x_train_vectorizer)
x_test_tfidf = tfidf.transform(x_test_vectorizer)

# =========================
# AdaBoost
# =========================

def start_adboost():
    from sklearn.ensemble import AdaBoostClassifier

    model = AdaBoostClassifier()
    model.fit(x_train_tfidf, y_train)

    y_pred = model.predict(x_test_tfidf)

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# SVM
# =========================

def start_svm():
    from sklearn.svm import SVC

    model = SVC()
    model.fit(x_train_tfidf, y_train)

    y_pred = model.predict(x_test_tfidf)

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# MLP
# =========================

def start_multi_layer_perceptron():
    from sklearn.neural_network import MLPClassifier

    model = MLPClassifier(hidden_layer_sizes=(10,10,10,10), verbose=True)
    model.fit(x_train_tfidf, y_train)

    y_pred = model.predict(x_test_tfidf)

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Random Forest
# =========================

def RandomForest():
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(n_estimators=200)
    model.fit(x_train_tfidf, y_train)

    y_pred = model.predict(x_test_tfidf)

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Gaussian Naive Bayes
# =========================

def GaussianNaiveBayes():
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()

    model.fit(x_train_tfidf.toarray(), y_train)

    y_pred = model.predict(x_test_tfidf.toarray())

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Decision Tree
# =========================

def DecisionTree():
    from sklearn.tree import DecisionTreeClassifier

    model = DecisionTreeClassifier()

    model.fit(x_train_tfidf.toarray(), y_train)

    y_pred = model.predict(x_test_tfidf.toarray())

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Logistic Regression
# =========================

def LogisticRegressionModel():
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()

    model.fit(x_train_tfidf.toarray(), y_train)

    y_pred = model.predict(x_test_tfidf.toarray())

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Gradient Boosting
# =========================

def GradientBoosting():
    from sklearn.ensemble import GradientBoostingClassifier

    model = GradientBoostingClassifier()

    model.fit(x_train_tfidf.toarray(), y_train)

    y_pred = model.predict(x_test_tfidf.toarray())

    cr = classification_report(y_test, y_pred, output_dict=True)
    cr = pd.DataFrame(cr).transpose()

    return cr.to_html()

# =========================
# Prediction Function
# =========================

df = pd.read_csv(path1, encoding="ISO-8859-1")

X_train, X_test, y_train, y_test = train_test_split(df['tweet'], df['class'], test_size=0.2, random_state=42)

count_vector = CountVectorizer(stop_words='english', lowercase=True)

training_data = count_vector.fit_transform(X_train)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(training_data, y_train)

def predict(message):

    message_vectorized = count_vector.transform([message])

    pred = model.predict(message_vectorized)

    if pred[0] == 1:
        msg = 'offensive'
    elif pred[0] == 0:
        msg = 'non-offensive'
    else:
        msg = 'neither'

    return msg