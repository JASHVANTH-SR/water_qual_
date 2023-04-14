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


        # Display the data types of each attribute
        print(df.dtypes)
        
        # Display the summary statistics of each attribute
        print(df.describe())
        
        # Display the summary statistics of each attribute
        print(df.describe())
        
        # Check for missing values
        print(df.isnull().sum())
        
        for col in df.columns:
            plt.figure()
            df.boxplot([col])
            plt.title(col)
            plt.show()


    

        
        

st.markdown('''### This is the **Study App** created in Streamlit using the **pandas-profiling** library.
****Credit:**** App built in `Python` + `Streamlit` by [JASHVANTH S R ](https://www.linkedin.com/in/jashvanth-s-r-476646213)[HARUL GANESH S B ](https://www.linkedin.com/in/harul-ganesh/)[BALAJI S ](https://www.linkedin.com/in/balaji-s-csbs-dept-03790a202/)[GOWTHAM H](https://www.linkedin.com/in/gowtham-haribabu-9425861bb/)
---
''')

# In[ ]:





