# In[1]:
import streamlit as st

import os
import time
import glob
from gtts import gTTS
from googletrans import Translator
from PIL import Image


import numpy as np
import pandas as pd
from warnings import filterwarnings
from collections import Counter

# Visualizations Libraries
import matplotlib.pyplot as plt
import plotly
import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

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



# Data Pre-processing Libraries
def app():
    try:
        os.mkdir("temp")
    except:
        pass
    colors_blue = ["#132C33", "#264D58", '#17869E', '#51C4D3', '#B4DBE9']
    colors_dark = ["#1F1F1F", "#313131", '#636363', '#AEAEAE', '#DADADA']
    colors_green = ['#01411C','#4B6F44','#4F7942','#74C365','#D0F0C0']
    translator = Translator()

    new_file = st.file_uploader("Choose an Excel file", type="xlsx")
    st.write('''[Example Excel(.xlsx) input file](https://docs.google.com/spreadsheets/d/1_u6TGnnj0Xs-Lkwde2H5MJ4i1o7Trixi/edit?usp=sharing&ouid=114232663325308153395&rtpof=true&sd=true)''')
    if new_file is not None:
        st.session_state.data = pd.read_excel(new_file, engine="openpyxl")    
        @st.cache(allow_output_mutation=True,suppress_st_warning=True)
        def load_excel():
            if "data" in st.session_state:
                return st.session_state.data
            else:
                return pd.DataFrame()
        df=load_excel()
        cor=df.corr()

        st.markdown("### Correlation between Variables used here")
        st.markdown("In statistics, correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data.")
        time.sleep(2)
        fig = px.imshow(cor,height=800,width=800,color_continuous_scale=colors_blue,template='plotly_white')

        fig.update_layout(font_family='monospace',
                        title=dict(text='Correlation Heatmap',x=0.5,y=0.93,
                                     font=dict(color=colors_dark[2],size=24)),
                        coloraxis_colorbar=dict(len=0.85,x=1.1) 
                         )

        st.plotly_chart(fig, use_container_width=True)


        # In[28]:


        df['NO2+NO3'].fillna(value=df['NO2+NO3'].median(),inplace=True)
        df['TDS'].fillna(value=df['TDS'].median(),inplace=True)
        df['Ca'].fillna(value=df['Ca'].median(),inplace=True)
        df['Mg'].fillna(value=df['Mg'].median(),inplace=True)
        df['Na'].fillna(value=df['Na'].median(),inplace=True)
        df['K'].fillna(value=df['K'].median(),inplace=True)
        df['Cl'].fillna(value=df['Cl'].median(),inplace=True)
        df['SO4'].fillna(value=df['SO4'].median(),inplace=True)
        df['CO3'].fillna(value=df['CO3'].median(),inplace=True)
        df['HCO3'].fillna(value=df['HCO3'].median(),inplace=True)
        df['F'].fillna(value=df['F'].median(),inplace=True)
        df['pH_GEN'].fillna(value=df['pH_GEN'].median(),inplace=True)
        df['EC_GEN'].fillna(value=df['EC_GEN'].median(),inplace=True)
        df['HAR_Total'].fillna(value=df['HAR_Total'].median(),inplace=True)
        df['SAR'].fillna(value=df['SAR'].median(),inplace=True)
        df['RSC'].fillna(value=df['RSC'].median(),inplace=True)
        df['Na%'].fillna(value=df['Na%'].median(),inplace=True)


        # In[47]:


        st.markdown('Data Types Present in Given Dataset')
        st.write(df.dtypes)
        
        
        # Display the summary statistics of each attribute
        st.markdown('Data Description and Statistical Details in Given Dataset')        
        st.write(df.describe())
        
        # Check for missing values
        st.markdown('Checks Presence of Null Data in Given Dataset')                
        st.write(df.isnull().sum())
        


    

        
        X = df[["TDS","NO2+NO3","Ca","Mg","Na","K","Cl","SO4","CO3","HCO3","F","pH_GEN","EC_GEN","HAR_Total","SAR","RSC","Na%","potability"]].drop('potability',axis=1).values
        y = df[["TDS","NO2+NO3","Ca","Mg","Na","K","Cl","SO4","CO3","HCO3","F","pH_GEN","EC_GEN","HAR_Total","SAR","RSC","Na%","potability"]]['potability'].values


        # In[48]:


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


        # In[53]:


        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)


        # In[56]:


        try:
            filterwarnings('ignore')
            models =[("LR", LogisticRegression(max_iter=1000)),("SVC", SVC()),('KNN',KNeighborsClassifier(n_neighbors=10)),
                     ("DTC", DecisionTreeClassifier()),("GNB", GaussianNB()),
                    ("SGDC", SGDClassifier()),("Perc", Perceptron()),("NC",NearestCentroid()),
                    ("Ridge", RidgeClassifier()),("NuSVC", NuSVC()),("BNB", BernoulliNB()),
                     ('RF',RandomForestClassifier()),('ADA',AdaBoostClassifier()),
                    ('XGB',GradientBoostingClassifier()),('PAC',PassiveAggressiveClassifier())]

            results = []
            names = []
            finalResults = []

            for name,model in models:
                model.fit(X_train, y_train)
                model_results = model.predict(X_test)
                score = precision_score(y_test, model_results,average='macro')
                results.append(score)
                names.append(name)
                finalResults.append((name,score))

            finalResults.sort(key=lambda k:k[1],reverse=True)
        except ValueError:
            print(' ')


        # In[57]:

        st.markdown("#### Best Algorithm for Supervised Machine Learning for our Data ")
        st.write(finalResults)

# In[ ]:





