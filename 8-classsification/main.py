from os import listdir
from os.path import isfile, join
import regex as r
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
import sklearn.metrics as skm
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

onlyfiles = [f for f in listdir("../dataset") if isfile(join("../dataset", f))]
n_amend = 0
amending = []
n_notamend = 0
not_amending = []
for f in onlyfiles: 
    with open(join("../dataset", f), encoding='utf-8') as _file:
        text = _file.read()
        text = text.lower()
        title_content = text.split("art. 1")
        title = title_content[0]
        content = "art. 1" + 'art. 1'.join(title_content[1:])
        header_splitted = title.split("ustawa")[0] + "ustawa"
        if len(r.findall(r'r.\s*o\s*zmianie\s*dataset', title)) > 0:
            n_amend += 1
            amending.append(header_splitted + content)
        else:
            n_notamend += 1
            not_amending.append(header_splitted + content)

print(len(amending))
print(len(not_amending))

X = amending + not_amending
y = [1] * len(amending) + [0] * len(not_amending)

X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)


def full_text(text):
    return text

def tenpercent(text):
    lines = [line for line in text.split("\n") if line != ""]
    return "\n".join(np.random.choice(lines, (len(lines)//10) + 1))

def tenlines(text):
    lines = [line for line in text.split("\n") if line != ""]
    return " ".join(np.random.choice(lines, 10))

def oneline(text):
    lines = [line for line in text.split("\n") if line != ""]
    return " ".join(np.random.choice(lines, 1))


def svm(X_train, X_val, X_test, y_train):

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer().fit(X_train + X_val + X_test)),
        ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
    ])
    parameters = {
        'tfidf__max_df': (0.25, 0.5, 0.75),
        'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }
    grid_search_tune = GridSearchCV(pipeline, parameters, cv=2, n_jobs=2, verbose=3)
    grid_search_tune.fit(X_train, y_train)

    return grid_search_tune.best_estimator_.predict(X_test)

for f in [tenpercent, oneline, tenpercent, full_text]:
    X_train_tmp = [f(x) for x in X_train]
    X_val_tmp = [f(x) for x in X_val]
    X_test_tmp = [f(x) for x in X_test]

    y_pred = svm(X_train_tmp, X_val_tmp, X_test_tmp, y_train)

    precision = skm.precision_score(y_test, y_pred)
    recall = skm.recall_score(y_test, y_pred)
    f1 = skm.f1_score(y_test, y_pred)

    with open("./svm/" + f.__name__, 'w', encoding='utf-8') as file_:
        file_.write("Precision: " + str(precision) + '\n')
        file_.write("Recall: " + str(recall) + '\n')
        file_.write("F1: " + str(f1) + '\n')
