import streamlit as st
from multiapp import MultiApp
from Water_qual import sample,sample2,qual_calc,eda,vlp1 # import your app modules here
from Water_qual import *
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split

# Modelling Libraries
from sklearn.linear_model import LogisticRegression,RidgeClassifier,SGDClassifier,PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.neighbors import KNeighborsClassifier,NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB,BernoulliNB
from sklearn.ensemble import VotingClassifier

# Evaluation & CV Libraries
from sklearn.metrics import precision_score,accuracy_score
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV,RepeatedStratifiedKFold

app1 = MultiApp()

# Add all your application here
app1.add_app("Individual Interpreter(Manual Upload)", sample.app)
app1.add_app("Individual Interpreter(Built in Dataset)", sample2.app)
app1.add_app("Summary Overall(Manual Upload)", vlp1.app)
app1.add_app("Water Quality calculator", qual_calc.app)
app1.add_app("Exploratory Data Analysis", eda.app)
app1.add_app("Querybot",chatbot.py)

app1.run()
