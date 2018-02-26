import numpy as np
import pandas as pd
import time
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier, BaggingClassifier, RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier

dontFit = ['score','title','subreddit']

with open('train.pickle', 'rb') as f:
    train = pickle.load(f)

X_train = train[0]
y_train = train[1]

xtr = X_train[[c for c in X_train if c not in dontFit]]

pd1 = {
        LogisticRegression:
    {'penalty':['l1','l2'], 'C' :np.linspace(.01, 100, num = 150)},
      DecisionTreeClassifier:
    {'criterion':['gini','entropy'],'max_depth':[None,1,2,3,4,5,6,7,8,9,10], 'min_samples_split':[2,3,4,5,6]},
      ExtraTreesClassifier:
    {'n_estimators':[2,5,10,15,20,40,60,75,100],'criterion':['gini','entropy'],
     'max_depth':[None,1,2,3,4,5,6,7,8,9,10], 'min_samples_split':[2,3,4,5,6]},
      BaggingClassifier:
    {'n_estimators':[2,5,10,15,20,40,60,75,100], 'max_samples':np.linspace(.01,1.0)},
      RandomForestClassifier:
    {'n_estimators':[2,5,10,15,20,40,60,75,100],'criterion':['gini','entropy'],
     'max_depth':[None,1,2,3,4,5,6,7,8,9,10], 'min_samples_split':[2,3,4,5,6]}
     }

GB1 = {
        GradientBoostingClassifier :{
            'loss' :['deviance','exponential'], 'learning_rate': np.linspace(.0001, .5, num = 50),
            'n_estimators': range(50,250,10), 'max_depth': range(2,5), 'max_features':[None]
            }
        }
GB2 = {
        GradientBoostingClassifier :{
            'loss' :['deviance','exponential'], 'learning_rate': np.linspace(.0001, .5, num = 50),
            'n_estimators': range(50,250,10), 'max_depth': range(2,5), 'max_features':['auto']
            }
        }
GB3 = {
        GradientBoostingClassifier :{
            'loss' :['deviance','exponential'], 'learning_rate': np.linspace(.0001, .5, num = 50),
            'n_estimators': range(50,250,10), 'max_depth': range(2,5), 'max_features':['log2']
            }
        }

pd2 = {
        AdaBoostClassifier: {
            'n_estimators': range(25,200)
        },
        BernoulliNB:{
            'alpha': np.linspace(.1, 5)
        },
        KNeighborsClassifier: {
            'n_neighbors' : range(3,50), 'weights': ['uniform','distance'], 'p' :[1,2]
        }
}

SVM1 = { SVC:{'C': np.logspace(-1,1, num=10), 'gamma' : np.logspace(-3, -1, num = 10)}}
SVM2 = { SVC:{'C': np.logspace(1,2, num=10), 'gamma' : np.logspace( -1, 1,num = 10)}}

def crossVal(clf, X, y, folds = 3):
    scores = []
    randOrd = np.random.permutation(len(y))
    slices = list(range(0,len(y)+1, int(len(y)/folds)))

    foldIndex = [randOrd[slice(slices[i],slices[i+1])] for i in range(folds) ]

    for tfi in foldIndex:
        y_test = y.loc[tfi]
        X_test = X.loc[tfi]

        notTfi = [fi for fi in foldIndex if (fi != tfi).any()]
        train = [item for sublist in notTfi for item in sublist]
        y_train = y.loc[train]
        X_train = X.loc[train]

        med, y_train = target(y_train)
        _, y_test = target(y_test, med)

        clf.fit(X_train, y_train)

        scores.append(clf.score(X_test, y_test))

    return scores

def target(data, commentsMed = 'calc'):

    if commentsMed == 'calc':
        commentsMed = np.median(data)

    return commentsMed, [c > commentsMed for c in data]


def searcher(paramDict, X, y):
    toRet = []

    for func in paramDict:
        tf0 = time.time()
        print(func)
        optionsDict = paramDict[func]
        toTry = dictCompile(optionsDict)
        for argDict in toTry:

            t0 = time.time()
            scores = crossVal(func(**argDict), X, y)
            t1 = time.time()
            name = dict({'name':str(func).split('.')[-1][:-2]}, **argDict)

            toRet.append((name, np.mean(scores), np.std(scores), t1-t0))
        print(time.time() - tf0)

    return toRet

def dictCompile(funcDict):
    individualDicts = []

    for k in funcDict:
        individualDicts.append([{k:v} for v in funcDict[k]])

    return dictMaker(individualDicts)

def dictMaker(lst):
    toRet = []
    for d in lst[0]:
        if len(lst)>1:
            for ds in dictMaker(lst[1:]):
                toRet.append(dict(d,**ds))
        else:
            return lst[0]
    return toRet


def doit():
    t0 = time.time()
    l = searcher(pd1,xtr, y_train)
    t1 = time.time()

    print('total', t1-t0)

    return l

def doit2():
    t0 = time.time()
    l = searcher(pd2, xtr, y_train)
    t1 - time.time()

    print('total', t1-t0)

    return l

def doit3():
    t0 = time.time()
    l = searcher(pd3, xtr, y_train)
    t1 - time.time()

    print('total', t1-t0)

    return l

mods2 = searcher(pd2, xtr, y_train)

with open('mods2.pickle', 'wb') as f:
    pickle.dump(mods2, f, protocol=0)
