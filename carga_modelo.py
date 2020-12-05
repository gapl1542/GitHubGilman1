import os
import re
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import numpy as np
import joblib


#Read all documents in a directory and its subdirectories


def read_all_documents(root):
    labels = []
    docs = []
    for r, dirs, files in os.walk(root):
        for file in files:
            with open(os.path.join(r, file), "r",encoding='utf-8') as f:
                docs.append(f.read())
            labels.append(r.replace(root, ''))
    return dict([('docs', docs), ('labels', labels)])


#Count words frequency in documents



def tokens(doc):
    return (tok.lower() for tok in re.findall(r"\w+", doc))

def frequency(tokens):
    f = defaultdict(int)
    for token in tokens:
        f[token] += 1
    return f

def tokens_frequency(doc):
    return frequency(tokens(doc))

#Extract features from documents
#Symbolic features names


def clasificador():
    data = read_all_documents('./training')
    documents = data['docs']
    labels = data['labels']

    vectorizer = DictVectorizer()
    vectorizer.fit_transform(tokens_frequency(d) for d in documents)

    vectorizer.get_feature_names()


#Sparse matrices
    hasher = FeatureHasher(n_features=2**8, input_type="string")
    X = hasher.transform(tokens(d) for d in documents)



#Train a text classifier using K-Means clustering


    clf = joblib.load('modelo_entrenado.pkl') # Carga del modelo.


    prepositions =['a','ante','bajo','cabe','con','contra','de','desde','en','entre','hacia','hasta','para','por','según','sin','so','sobre','tras']
    prep_alike = ['durante','mediante','excepto','salvo','incluso','más','menos']
    adverbs = ['no','si','sí']
    articles = ['el','la','los','las','un','una','unos','unas','este','esta','estos','estas','aquel','aquella','aquellos','aquellas']
    aux_verbs = ['he','has','ha','hemos','habéis','han','había','habías','habíamos','habíais','habían']
    tfid = TfidfVectorizer(stop_words=prepositions+prep_alike+adverbs+articles+aux_verbs)

    X_train = tfid.fit_transform(documents)
    y_train = labels

    #Predict categories for new articles

    test = read_all_documents('prueba')
    X_test = tfid.transform(test['docs'])
    y_test = test['labels']
    pred = clf.predict(X_test)
    cat = str(pred[0])
    return(cat)
