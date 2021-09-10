# Predicts diseases based on the symptoms entered and selected by the user.
# importing all necessary libraries
import warnings
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split, cross_val_score
from statistics import mean
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from itertools import combinations
from time import time
from collections import Counter
import operator
from xgboost import XGBClassifier
import math
from Treatment import diseaseDetail
from sklearn.linear_model import LogisticRegression

warnings.simplefilter("ignore")

# import nltk
# nltk.download('all')

# utlities for pre-processing
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
splitter = RegexpTokenizer(r'\w+')

# Load Dataset scraped from NHP (https://www.nhp.gov.in/disease-a-z) & Wikipedia
# Scrapping and creation of dataset csv is done in a separate program
df_comb = pd.read_csv("dis_sym_dataset_comb.csv")   # Disease combination
df_norm = pd.read_csv("dis_sym_dataset_norm.csv")   # Individual Disease

X = df_comb.iloc[:, 1:]
Y = df_comb.iloc[:, 0:1]

"""Using **Logistic Regression (LR) Classifier** as it gives better accuracy compared to other classification models as observed in the comparison of model accuracies in Model_latest.py

Cross validation is done on dataset with cv = 5
"""

lr = LogisticRegression()
lr = lr.fit(X, Y)
scores = cross_val_score(lr, X, Y, cv=5)

X = df_norm.iloc[:, 1:]
Y = df_norm.iloc[:, 0:1]

# List of symptoms
dataset_symptoms = list(X.columns)

# Taking symptoms from user as input
def disease_prediction_rasa(rasa_symp):
    user_symptoms = str(rasa_symp).lower().split(',')
    # Preprocessing the input symptoms
    processed_user_symptoms = []
    for sym in user_symptoms:
        sym = sym.strip()
        sym = sym.replace('-', ' ')
        sym = sym.replace("'", '')
        sym = ' '.join([lemmatizer.lemmatize(word) for word in splitter.tokenize(sym)])
        processed_user_symptoms.append(sym)

    # Loop over all the symptoms in dataset and check its similarity score to the synonym string of the user-input
    # symptoms. If similarity>0.5, add the symptom to the final list
    found_symptoms = set()
    for idx, data_sym in enumerate(dataset_symptoms):
        data_sym_split = data_sym.split()
        for user_sym in user_symptoms:
            count = 0
            for symp in data_sym_split:
                if symp in user_sym.split():
                    count += 1
            if count/len(data_sym_split) > 0.5:
                found_symptoms.add(data_sym)
    found_symptoms = list(found_symptoms)
    # print(found_symptoms)

    """Final Symptom list"""

    # Create query vector based on symptoms selected by the user
    # print("\nFinal list of Symptoms that will be used for prediction:")
    sample_x = [0 for x in range(0, len(dataset_symptoms))]
    for val in found_symptoms:
        # print(val)
        sample_x[dataset_symptoms.index(val)] = 1

    """Prediction of disease is done"""

    # Predict disease
    lr = LogisticRegression()
    lr = lr.fit(X, Y)
    prediction = lr.predict_proba([sample_x])

    """Show top k diseases and their probabilities to the user.

    K in this case is 10
    """

    k = 4
    diseases = list(set(Y['label_dis']))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]
    dName = []
    dProb = []
    """# **Showing the list of top k diseases to the user with their prediction probabilities.**

    # **For getting information about the suggested treatments, user can enter the corresponding index to know more details.**
    """

    # print(f"\nTop {k} diseases predicted based on symptoms")
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df_norm.loc[df_norm['label_dis'] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(dataset_symptoms[idx])
        prob = (len(match_sym.intersection(set(found_symptoms)))+1)/(len(set(found_symptoms))+1)
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key]*100
        # print(str(j) + " Disease name:", diseases[key], "\tProbability:", str(round(prob, 2))+"%")
        topk_index_mapping[j] = key
        j += 1
        diseaseName = diseases[key]
        diseaseProbability = str(round(prob, 2))
        dName.append(diseaseName)
        dProb.append(diseaseProbability)


    # for i in range(0, len(dName)):
    #     print(dName[i]),
    #
    # for a in range(0, len(dProb)):
    #     print(dProb[a]),

    try:
        if len(dName) != 0:
            return dName, dProb
        else:
            return "Failed", "Failed"

    except TypeError:
        return "Failed", "Failed"

    return dName, dProb


# result_dName, result_dProb = disease_prediction_rasa("fever,cold,vomiting,tiredness,headache")
# for s in range(0, len(result_dName)):
#     print(result_dName[s])