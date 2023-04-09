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
import seaborn as sns
import plotly
import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import missingno as msno

# Data Pre-processing Libraries
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


# In[2]:
st.set_page_config(page_title="Water Quality", page_icon="🌾", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_option('deprecation.showPyplotGlobalUse', False)
#To ensure that the uploaded file is not shared between different users or sessions, you can use the SessionState utility from Streamlit to create a session-specific state object that can be used to store the uploaded file. Here's an updated version of the code that uses SessionState:


#python
#Copy code
import hashlib


# Define the function to load the Excel file and cache the data

# Define the Streamlit app

try:
    os.mkdir("temp")
except:
    pass



# In[3]:
translator = Translator()
st.title('''
The Water Quality Analysis App''')

image = Image.open('tvalluvar.jpeg')
st.image(image)
st.markdown("நீரின்று அமையாது உலகெனின் யார்யார்க்கும்") 
st.markdown("வானின்று அமையாது ஒழுக்கு")

input_language="en"
in_lang = st.selectbox(
    "Select your output language",
    ("English", "Tamil", "Telugu", "Hindi", "Malayalam", "Kannada"),)
text = "Welcome To Water Quality Analysis Software"
if in_lang == "English":
    output_language = "en"
elif in_lang == "Tamil":
    output_language = "ta"
elif in_lang == "Telugu":
    output_language = "te"
elif in_lang == "Hindi":
    output_language = "hi"
elif in_lang == "Malayalam":
    output_language = "ml"
elif in_lang == "Kannada":
    output_language = "kn"

def text_to_speech(input_language, output_language, text):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

def runvoice(text):
    try:
        result, output_text = text_to_speech(input_language, output_language, text)
        audio_file = open(f"temp/{result}.mp3", "rb+")
        audio_bytes = audio_file.read()
        time.sleep(2)
        st.audio(audio_bytes, format="audio/mp3",start_time=0)
        st.write(f" {output_text}")
    except Exception as e:
        print()


image = Image.open('tree.jpg')
st.image(image)




runvoice("The Water Quality Analysis App")


runvoice("This is the Software used to study the Characteristics of Water. This software is created in Streamlit using Scikit-learn and plotly package.\
    Courtesy :  Software built in 'Python' and 'Streamlit' by JASHVANTH S R,BALAJI S,HARUL GANESH S B,GOWTHAM H")
time.sleep(2)
colors_blue = ["#132C33", "#264D58", '#17869E', '#51C4D3', '#B4DBE9']
colors_dark = ["#1F1F1F", "#313131", '#636363', '#AEAEAE', '#DADADA']
colors_green = ['#01411C','#4B6F44','#4F7942','#74C365','#D0F0C0']

new_file = st.file_uploader("Choose an Excel file", type="xlsx")
st.write('''[Example Excel(.xlsx) input file](https://docs.google.com/spreadsheets/d/1_u6TGnnj0Xs-Lkwde2H5MJ4i1o7Trixi/edit?usp=sharing&ouid=114232663325308153395&rtpof=true&sd=true)''')
if new_file is not None:
    st.session_state.data = pd.read_excel(new_file, engine="openpyxl")    
    @st.cache_data(allow_output_mutation=True,suppress_st_warning=True)    
    
    def load_excel():
        if "data" in st.session_state:
            return st.session_state.data
        else:
            return pd.DataFrame()
    df=load_excel()
    st.markdown("The input dataset's first 5 rows")    
    st.write(df.head())


        # In[6]:

    st.markdown("### Potability")
    st.markdown("It defines about a liquid that is suitable for drinking or not. Parameters for drinking water quality typically fall within three categories: physical, chemical, microbiological.")
    st.markdown("Physical and chemical parameters include heavy metals, trace organic compounds, total suspended solids, and turbidity. Chemical parameters tend to pose more of a chronic health risk through buildup of heavy metals although some components like nitrates/nitrites and arsenic can have a more immediate impact. Physical parameters affect the aesthetics and taste of the drinking water and may complicate the removal of microbial pathogens.")
    runvoice("It defines about a liquid that is suitable for drinking or not. Parameters\
     for drinking water quality typically fall within three categories: physical, chemical,\
      microbiological.Physical and chemical parameters include heavy metals, trace organic compounds,\
       total suspended solids, and turbidity. Chemical parameters tend to pose more of a chronic health risk through\
        buildup of heavy metals although some components like nitrates/nitrites and arsenic can have a more immediate\
         impact. Physical parameters affect the aesthetics and taste of the drinking water and may complicate the removal of microbial pathogens.")
    time.sleep(2)
    d= pd.DataFrame(df['potability'].value_counts())
    fig = px.pie(d,values='potability',names=['Not Potable','Potable'],hole=0.4,opacity=0.6,
                color_discrete_sequence=[colors_green[3],colors_blue[3]],
                 labels={'label':'Potability','Potability':'No. Of Samples'})

    fig.add_annotation(text='We can resample the data<br> to get a balanced dataset',
                       x=1.2,y=0.9,showarrow=False,font_size=12,opacity=0.7,font_family='monospace')
    fig.add_annotation(text='Potability',
                       x=0.5,y=0.5,showarrow=False,font_size=14,opacity=0.7,font_family='monospace')

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Q. How many samples of water are Potable?',x=0.47,y=0.98,
                   font=dict(color=colors_dark[2],size=20)),
        legend=dict(x=0.37,y=-0.05,orientation='h',traceorder='reversed'),
        hoverlabel=dict(bgcolor='white'))

    fig.update_traces(textposition='outside', textinfo='percent+label')

    st.plotly_chart(fig)


    # In[7]:

    st.markdown("### Total Dissolved Solids")
    st.image(Image.open("SOLIDS IN WATER.jpg"))
    st.markdown("Total dissolved solids (TDS) is a measure of the dissolved combined content of all inorganic and organic substances present in a liquid in molecular,\
     ionized, or micro-granular (colloidal sol) suspended form.\
     TDS concentrations are often reported in parts per million (ppm). Water TDS concentrations can be determined using a digital meter.")
    runvoice("Total dissolved solids (TDS) is a measure of the dissolved combined content of all inorganic and organic substances present in a liquid in molecular,\
     ionized, or micro-granular (colloidal sol) suspended form.\
     TDS concentrations are often reported in parts per million (ppm). Water TDS concentrations can be determined using a digital meter.")
    time.sleep(2)
    fig = px.histogram(df,x='TDS',y=df['TDS'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=301, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
    fig.add_vline(x=601, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
    fig.add_vline(x=901, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
    fig.add_vline(x=1201, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='<300 is considered as excellent',x=250,y=30,showarrow=False,font_size=12)
    fig.add_annotation(text='>300 and <600 is good',x=400,y=40,showarrow=False,font_size=12)
    fig.add_annotation(text='>600 and <900 is fair',x=750,y=50,showarrow=False,font_size=12)
    fig.add_annotation(text='>900 and <1200 is poor',x=1050,y=60,showarrow=False,font_size=12)
    fig.add_annotation(text='>1200 is unacceptable',x=1250,y=70,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Distribution Of Total Dissolved Solids',x=0.5,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Dissolved Solids (ppm)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[8]:

    st.markdown("### Nitrite and Nitrate")
    st.image(Image.open("no2no3.jpg"))
    st.markdown("Nitrates and nitrites are compounds that occur naturally in the human body and some foods, such as vegetables. Manufacturers also add them to processed foods, such as bacon, to preserve them and make them last longer.\
        some forms, nitrates and nitrites can be hazardous. However, they may also have health benefits.")
    runvoice("Nitrates and nitrites are compounds that occur naturally in the human body and some foods, such as vegetables. Manufacturers also add them to processed foods, such as bacon, to preserve them and make them last longer.\
    In some forms, nitrates and nitrites can be hazardous. However, they may also have health benefits.")
    time.sleep(2)    
    fig = px.histogram(df,x='NO2+NO3',y=df['NO2+NO3'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=21, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='NO2+NO3 should not exceed 20mg/L',x=20,y=75,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='NO2+NO3',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='NO2+NO3 (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[9]:

    st.markdown("### Calcium")
    st.image(Image.open("Ca.png"))
    st.markdown("Calcium is a chemical element with the symbol Ca and atomic number 20. As an alkaline earth metal, calcium is a reactive metal that forms a dark oxide-nitride layer when exposed to air.\
     Calcium is a mineral your body needs to build and maintain strong bones and to carry out many important functions. Calcium is the most abundant mineral in the body. Almost all calcium in the body is stored in bones and teeth, giving them structure and hardness.")
    runvoice("Calcium is a chemical element with the symbol Ca and atomic number 20. As an alkaline earth metal, calcium is a reactive metal that forms a dark oxide-nitride layer when exposed to air.\
     Calcium is a mineral your body needs to build and maintain strong bones and to carry out many important functions. Calcium is the most abundant mineral in the body. Almost all calcium in the body is stored in bones and teeth, giving them structure and hardness.")
    time.sleep(2)    
    fig = px.histogram(df,x='Ca',y=df['Ca'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Calcium',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Ca (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[10]:

    st.markdown("### Magnesium")
    st.image(Image.open("Magnesium.png"))
    st.markdown("Magnesium is a chemical element with the symbol Mg and atomic number 12. It is a shiny gray metal having a low density, low melting point and high chemical reactivity.\
        Magnesium is a cofactor in more than 300 enzyme systems that regulate diverse biochemical reactions in the body, including protein synthesis, muscle and nerve function, blood glucose control, and blood pressure regulation [1-3]. Magnesium is required for energy production, oxidative phosphorylation, and glycolysis.")
    runvoice("Magnesium is a chemical element with the symbol Mg and atomic number 12. It is a shiny gray metal having a low density, low melting point and high chemical reactivity.\
        Magnesium is a cofactor in more than 300 enzyme systems that regulate diverse biochemical reactions in the body, including protein synthesis, muscle and nerve function, blood glucose control, and blood pressure regulation [1-3]. Magnesium is required for energy production, oxidative phosphorylation, and glycolysis.")
    time.sleep(2)    
    fig = px.histogram(df,x='Mg',y=df['Mg'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=37.5, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='Mg should not exceed 37.5mg/L',x=38,y=75,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Magnesium',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Mg (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[11]:

    st.markdown("### Sodium")
    st.image("Na.png")
    st.markdown("Sodium is a chemical element with the symbol Na and atomic number 11. It is a soft, silvery-white, highly reactive metal. Sodium is an alkali metal, being in group 1 of the periodic table. Its only stable isotope is ²³Na. \
        It helps with the function of nerves and muscles. It also helps to keep the right balance of fluids in your body. Your kidneys control how much sodium is in your body. If you have too much and your kidneys can't get rid it, sodium builds up in your blood. This can lead to high blood pressure.")
    runvoice("Sodium is a chemical element with the symbol Na and atomic number 11. It is a soft, silvery-white, highly reactive metal. Sodium is an alkali metal, being in group 1 of the periodic table. Its only stable isotope is ²³Na. \
        It helps with the function of nerves and muscles. It also helps to keep the right balance of fluids in your body. Your kidneys control how much sodium is in your body. If you have too much and your kidneys can't get rid it, sodium builds up in your blood. This can lead to high blood pressure.")
    time.sleep(2)    
    fig = px.histogram(df,x='Na',y=df['Na'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Sodium',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Na (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[12]:

    st.markdown("### Potassium")
    st.image(Image.open("K.png"))
    st.markdown("Potassium is the chemical element with the symbol K and atomic number 19. It is a silvery white metal that is soft enough to easily cut with a knife.\
        Potassium is an essential mineral that is needed by all tissues in the body. It is sometimes referred to as an electrolyte because it carries a small electrical charge that activates various cell and nerve functions. Potassium is found naturally in many foods and as a supplement.")
    runvoice("Potassium is the chemical element with the symbol K and atomic number 19. It is a silvery white metal that is soft enough to easily cut with a knife.\
        Potassium is an essential mineral that is needed by all tissues in the body. It is sometimes referred to as an electrolyte because it carries a small electrical charge that activates various cell and nerve functions. Potassium is found naturally in many foods and as a supplement.")
    time.sleep(2)    
    fig = px.histogram(df,x='K',y=df['K'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')
    fig.update_layout(
        font_family='monospace',
        title=dict(text='Potassium',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='K (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[13]:

    st.markdown("### Chlorine")
    st.image(Image.open("Cl.png"))
    st.markdown("Chlorine is a chemical element with the symbol Cl and atomic number 17. The second-lightest of the halogens, it appears between fluorine and bromine in the periodic table and its properties are mostly intermediate between them.\
        Chlorine has a pungent, irritating odor similar to bleach that is detectable at low concentrations. The density of chlorine gas is approximately 2.5 times greater than air, which will cause it to initially remain near the ground in areas with little air movement.")
    runvoice("Chlorine is a chemical element with the symbol Cl and atomic number 17. The second-lightest of the halogens, it appears between fluorine and bromine in the periodic table and its properties are mostly intermediate between them.\
        Chlorine has a pungent, irritating odor similar to bleach that is detectable at low concentrations. The density of chlorine gas is approximately 2.5 times greater than air, which will cause it to initially remain near the ground in areas with little air movement.")
    time.sleep(2)    
    fig = px.histogram(df,x='Cl',y=df['Cl'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=251, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='Cl should not exceed 250mg/L',x=20,y=75,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Chlorine',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Cl (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[14]:
    st.markdown("### Sulphate")
    st.image(Image.open("Sulfate-ion.png"))
    st.markdown("The sulfate or sulphate ion is a polyatomic anion with the empirical formula SO2−4. Salts, acid derivatives, and peroxides of sulfate are widely used in industry. Sulfates occur widely in everyday life. Sulfates are salts of sulfuric acid and many are prepared from that acid. ")
    runvoice("The sulfate or sulphate ion is a polyatomic anion with the empirical formula SO2−4. Salts, acid derivatives, and peroxides of sulfate are widely used in industry. Sulfates occur widely in everyday life. Sulfates are salts of sulfuric acid and many are prepared from that acid. ")
    time.sleep(2)
    fig = px.histogram(df,x='SO4',y=df['SO4'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=201, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='SO4 should not exceed 250mg/L',x=20,y=75,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Sulphate',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='SO4 (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[15]:

    st.markdown("### Carbonate")
    st.image(Image.open("co3.png"))
    st.markdown("A carbonate is a salt of carbonic acid, characterized by the presence of the carbonate ion, a polyatomic ion with the formula CO2−3. The word carbonate may also refer to a carbonate ester, an organic compound containing the carbonate group C(O–)")
    runvoice("A carbonate is a salt of carbonic acid, characterized by the presence of the carbonate ion, a polyatomic ion with the formula CO2−3. The word carbonate may also refer to a carbonate ester, an organic compound containing the carbonate group C(O–)")
    time.sleep(2)    
    fig = px.histogram(df,x='CO3',y=df['CO3'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')
    fig.update_layout(
        font_family='monospace',
        title=dict(text='Carbonate',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='CO3 (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[16]:

    st.markdown("### Bi-Carbonate")
    st.image(Image.open("Bicarbonate-resonance.png"))
    st.markdown("In inorganic chemistry, bicarbonate is an intermediate form in the deprotonation of carbonic acid. It is a polyatomic anion with the chemical formula HCO⁻ ₃. Bicarbonate serves a crucial biochemical role in the physiological pH buffering system.\
        It's a byproduct of your body's metabolism. Our blood brings bicarbonate to our lungs, and then it is exhaled as carbon dioxide. Our kidneys also help regulate bicarbonate. Bicarbonate is excreted and reabsorbed by our kidneys.")
    runvoice("In inorganic chemistry, bicarbonate is an intermediate form in the deprotonation of carbonic acid. It is a polyatomic anion with the chemical formula HCO⁻ ₃. Bicarbonate serves a crucial biochemical role in the physiological pH buffering system.\
        It's a byproduct of your body's metabolism. Our blood brings bicarbonate to our lungs, and then it is exhaled as carbon dioxide. Our kidneys also help regulate bicarbonate. Bicarbonate is excreted and reabsorbed by our kidneys.")
    time.sleep(2)    
    fig = px.histogram(df,x='HCO3',y=df['HCO3'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=401, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='HCO3 should not exceed 400mg/L',x=400,y=32,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Bi-Carbonate',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='HCO3 (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[17]:

    st.markdown("### Fluorine")
    st.image(Image.open("Fluorine_Tile.png"))
    st.markdown("Fluorine is a chemical element with the symbol F and atomic number 9. It is the lightest halogen and exists at standard conditions as a highly toxic, pale yellow diatomic gas. As the most electronegative reactive element, it is extremely reactive, as it reacts with all other elements except for the light inert gases.\
        Fluorine is a nonmetallic, pale yellow-green gaseous element with a pungent odor. It is the most electronegative and reactive of all the elements. Fluorine is an element that is widely distributed in the environment, but because of its high reactivity it is not found naturally in its elemental state.")
    runvoice("Fluorine is a chemical element with the symbol F and atomic number 9. It is the lightest halogen and exists at standard conditions as a highly toxic, pale yellow diatomic gas. As the most electronegative reactive element, it is extremely reactive, as it reacts with all other elements except for the light inert gases.\
        Fluorine is a nonmetallic, pale yellow-green gaseous element with a pungent odor. It is the most electronegative and reactive of all the elements. Fluorine is an element that is widely distributed in the environment, but because of its high reactivity it is not found naturally in its elemental state.")
    time.sleep(2)    
    fig = px.histogram(df,x='F',y=df['F'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=1, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='Fluorine should not exceed 1mg/L',x=1.5,y=35,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Fluorine',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='F (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[18]:

    st.markdown("### pH Level Distribution")
    st.image(Image.open("PH_scale_3.jpg"))
    st.markdown("In chemistry, pH, also referred to as acidity, historically denoting 'potential of hydrogen', is a scale used to specify the acidity or basicity of an aqueous solution. Acidic solutions are measured to have lower pH values than basic or alkaline solutions.")
    runvoice("In chemistry, pH, also referred to as acidity, historically denoting 'potential of hydrogen', is a scale used to specify the acidity or basicity of an aqueous solution. Acidic solutions are measured to have lower pH values than basic or alkaline solutions.")
    time.sleep(2)
    fig = px.histogram(df,x='pH_GEN',y=df['pH_GEN'],color='potability',template='plotly_white',
                  marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                  barmode='group',histfunc='count')

    fig.add_vline(x=7, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='<7 is Acidic',x=4,y=70,showarrow=False,font_size=13)
    fig.add_annotation(text='>7 is Basic',x=10,y=70,showarrow=False,font_size=13)


    fig.update_layout(
        font_family='monospace',
        title=dict(text='pH Level Distribution',x=0.5,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='pH Level',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[19]:

    st.markdown("### Electrical Conductivity")
    st.image(Image.open("ec.jpg"))
    st.markdown("The conductivity of water is a measure of the capability of water to pass electrical flow. This ability directly depends on the concentration of conductive ions in the water.")
    runvoice("The conductivity of water is a measure of the capability of water to pass electrical flow. This ability directly depends on the concentration of conductive ions in the water.")
    time.sleep(2)    
    fig = px.histogram(df,x='EC_GEN',y=df['EC_GEN'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=1500, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='EC should not exceed 1500 µS/cm',x=1500,y=32,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Electrical Conductivity',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='EC (µS/cm)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[20]:

    st.markdown("### Hardness Distribution")
    st.image("hardness-of-water-1.png")
    st.markdown("Hard water is water that has high mineral content. Hard water is formed when water percolates through deposits of limestone, chalk or gypsum, which are largely made up of calcium and magnesium carbonates, bicarbonates and sulfates. Hard drinking water may have moderate health benefits. ")
    runvoice("Hard water is water that has high mineral content. Hard water is formed when water percolates through deposits of limestone, chalk or gypsum, which are largely made up of calcium and magnesium carbonates, bicarbonates and sulfates. Hard drinking water may have moderate health benefits. ")
    time.sleep(2)
    fig = px.histogram(df,x='HAR_Total',y=df['HAR_Total'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=151, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
    fig.add_vline(x=301, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
    fig.add_vline(x=76, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='<76 mg/L is considered soft',x=75,y=30,showarrow=False,font_size=12)
    fig.add_annotation(text='Between 76 and 150 (mg/L) is moderately hard',x=120,y=40,showarrow=False,font_size=12)
    fig.add_annotation(text='Between 151 and 300 (mg/L) is considered hard',x=180,y=50,showarrow=False,font_size=12)
    fig.add_annotation(text='>300 mg/L is considered very hard',x=310,y=60,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Hardness Distribution',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Hardness (mg/L)',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[21]:

    st.markdown("### Sodium Adsorption Ratio")
    st.image(Image.open("sar.png"))
    st.markdown("Sodium adsorption ratio (SAR) means a value representing the relative amount of sodium ions to the combined amount of calcium and magnesium ions in water using the following formula: SAR = [Na]/(([Ca]+[Mg])/2)1/2, where all concentrations are expressed as milliequivalents of charge per liter.")
    runvoice("Sodium adsorption ratio (SAR) means a value representing the relative amount of sodium ions to the combined amount of calcium and magnesium ions in water using the following formula: SAR = [Na]/(([Ca]+[Mg])/2)1/2, where all concentrations are expressed as milliequivalents of charge per liter.")
    time.sleep(2)    
    fig = px.histogram(df,x='SAR',y=df['SAR'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=26, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='SAR should not exceed 26 (mmoles l−1)0.5',x=27,y=32,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Sodium Adsorption Ratio',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='SAR (mmoles l−1)0.5',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[22]:

    st.markdown("### Residual Sodium Carbonate")
    st.image(Image.open("eqn_rsc.png"))
    st.markdown("Residual sodium carbonate (RSC) is a common means of assessing the sodium permeability hazard, and takes into account the bicarbonate/carbonate and calcium/magnesium concentrations in irrigation water")
    runvoice("Residual sodium carbonate (RSC) is a common means of assessing the sodium permeability hazard, and takes into account the bicarbonate/carbonate and calcium/magnesium concentrations in irrigation water")
    time.sleep(2)    
    fig = px.histogram(df,x='RSC',y=df['RSC'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')

    fig.add_vline(x=2.5, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

    fig.add_annotation(text='RSC should not exceed 2.5',x=2.6,y=32,showarrow=False,font_size=12)

    fig.update_layout(
        font_family='monospace',
        title=dict(text='Residual Sodium Carbonate',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='RSC',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[23]:

    st.markdown("### Percentage of Sodium Dissolved")
    st.image(Image.open("nap.png"))
    st.markdown("It says the amount of Sodium Dissolved in liquid in terms of Percentage")
    runvoice("It says the amount of Sodium Dissolved in liquid in terms of Percentage")
    time.sleep(2)    
    fig = px.histogram(df,x='Na%',y=df['Na%'],color='potability',template='plotly_white',
                      marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                      barmode='group',histfunc='count')
    fig.update_layout(
        font_family='monospace',
        title=dict(text='Percentage of Sodium Dissolved',x=0.53,y=0.95,
                   font=dict(color=colors_dark[2],size=20)),
        xaxis_title_text='Na%',
        yaxis_title_text='Count',
        legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


    # In[24]:


    rslt_df = df[df['potability'] == 1]


    # In[25]:


    rslt_df


    # In[26]:


    cor=df.corr()


    # In[27]:

    st.markdown("### Correlation between Variables used here")
    st.markdown("In statistics, correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data.")
    runvoice("In statistics, correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data.")
    time.sleep(2)
    fig = px.imshow(cor,height=800,width=800,color_continuous_scale=colors_blue,template='plotly_white')

    fig.update_layout(font_family='monospace',
                    title=dict(text='Correlation Heatmap',x=0.5,y=0.93,
                                 font=dict(color=colors_dark[2],size=24)),
                    coloraxis_colorbar=dict(len=0.85,x=1.1) 
                     )

    st.plotly_chart(fig, use_container_width=True)


    # In[28]:

    fig = msno.matrix(df,color=(0,0.5,0.5))


    # In[29]:


    df.isnull().sum()


    # In[30]:

    st.markdown("#### Details of Parameters which leads potability to O")
    runvoice("Details of Parameters which leads potability to O")
    time.sleep(2)    
    st.write(df[df['potability']==0].describe())


    # In[31]:

    st.markdown("#### Details of Parameters which leads potability to 1")    
    runvoice("Details of Parameters which leads potability to 1")
    time.sleep(2)    
    st.write(df[df['potability']==1].describe())


    # In[52]:


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


    X = df[["TDS","NO2+NO3","Ca","Mg","Na","K","Cl","SO4","CO3","HCO3","F","pH_GEN","EC_GEN","HAR_Total","SAR","RSC","Na%","potability"]].drop('potability',axis=1).values
    y = df[["TDS","NO2+NO3","Ca","Mg","Na","K","Cl","SO4","CO3","HCO3","F","pH_GEN","EC_GEN","HAR_Total","SAR","RSC","Na%","potability"]]['potability'].values


    # In[48]:


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


    # In[53]:


    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)


    if st.button('Individual Details of Well'):
        df['Date of collection'] = pd.to_datetime(df['Date of collection']).dt.strftime('%Y-%m-%d %H:%M:%S')
        # Set up Plotly figure
        well_nos = df["Well No"].unique()
        tahsils = df["Tahsil / Taluk"].unique()
        params = ["TDS", "NO2+NO3", "Ca", "Mg", "Na", "K", "Cl", "SO4", "CO3", "HCO3", "F", "pH_GEN", "EC_GEN", "HAR_Total", "SAR", "RSC", "Na%"]

        # Create the streamlit app
        st.title("Water Potability Dataset")

        # Choose the Tahsil / Taluk, Well No and parameter
        tahsil = st.selectbox("Choose a Tahsil / Taluk", tahsils)
        filtered_df = df[(df["Tahsil / Taluk"] == tahsil)]
        well_no = st.selectbox("Choose a Well No", filtered_df["Well No"].unique())
        param = st.selectbox("Choose a parameter", params)

        # Filter the dataset for the chosen Well No and parameter
        filtered_df = filtered_df[(filtered_df["Well No"] == well_no)][["Date of collection", param, "potability"]]

        # Plot the animated representation of the chosen parameter for the chosen well
        fig = px.scatter(filtered_df, x="Date of collection", y=param, color="potability", range_y=[0, filtered_df[param].max()], text=param)
        fig.update_traces(mode="markers", hovertemplate="Date: %{x}<br>Value: %{text:.2f}")
        fig.update_layout(title=f"{param} for Well No {well_no} in {tahsil}", xaxis_title="Date of collection", yaxis_title=param, showlegend=True)

        # Show the plot
        st.plotly_chart(fig)

        # Show the potability classification for the chosen well and parameter
        st.write(f"Potability of Well No {well_no} for {param}:")
        for date, potability in filtered_df[["Date of collection", "potability"]].itertuples(index=False):
            st.write(f"- Date: {date}, Potability: {potability}")



    # In[56]:

    if st.button('Wanna Check Accuracy oF Data'):
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
        st.markdown("#### Best Algorithm for Supervised Machine Learning for our Data ")
        runvoice("Best Algorithm for Supervised Machine Learning for our Data")

        finalResults
else:
        st.info('Awaiting for Excel file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            runvoice(text="Press to use Example Dataset")
            @st.cache_data(allow_output_mutation=True,suppress_st_warning=True)
            def load_excel(selected_option):
                if selected_option == 'Chengalpattu':
                    return pd.read_excel("cgl.xlsx", engine="openpyxl")
                elif selected_option == 'Kancheepuram':
                    return pd.read_excel("kanch.xlsx", engine="openpyxl")
                elif selected_option == 'Thiruvallur':
                    return pd.read_excel("trl.xlsx", engine="openpyxl")
                elif selected_option == 'Villupuram':
                    return pd.read_excel("vlp.xlsx", engine="openpyxl")
                elif selected_option == 'vellore':
                    return pd.read_excel("vlr.xlsx", engine="openpyxl")
                else:
                    return pd.DataFrame()

            selected_option = st.selectbox(
                "Select an Example District based Dataset:",
                ("Chengalpattu", "Kancheepuram", "Thiruvallur", "Villupuram", "vellore"),
            )

            df = load_excel(selected_option)
                    # In[4]:




            # In[5]:
            st.markdown("The input dataset's first 5 rows")    
            st.write(df.head())


                # In[6]:

            st.markdown("### Potability")
            st.markdown("It defines about a liquid that is suitable for drinking or not. Parameters for drinking water quality typically fall within three categories: physical, chemical, microbiological.")
            st.markdown("Physical and chemical parameters include heavy metals, trace organic compounds, total suspended solids, and turbidity. Chemical parameters tend to pose more of a chronic health risk through buildup of heavy metals although some components like nitrates/nitrites and arsenic can have a more immediate impact. Physical parameters affect the aesthetics and taste of the drinking water and may complicate the removal of microbial pathogens.")
            runvoice("It defines about a liquid that is suitable for drinking or not. Parameters\
             for drinking water quality typically fall within three categories: physical, chemical,\
              microbiological.Physical and chemical parameters include heavy metals, trace organic compounds,\
               total suspended solids, and turbidity. Chemical parameters tend to pose more of a chronic health risk through\
                buildup of heavy metals although some components like nitrates/nitrites and arsenic can have a more immediate\
                 impact. Physical parameters affect the aesthetics and taste of the drinking water and may complicate the removal of microbial pathogens.")
            time.sleep(2)
            d= pd.DataFrame(df['potability'].value_counts())
            fig = px.pie(d,values='potability',names=['Not Potable','Potable'],hole=0.4,opacity=0.6,
                        color_discrete_sequence=[colors_green[3],colors_blue[3]],
                         labels={'label':'Potability','Potability':'No. Of Samples'})

            fig.add_annotation(text='We can resample the data<br> to get a balanced dataset',
                               x=1.2,y=0.9,showarrow=False,font_size=12,opacity=0.7,font_family='monospace')
            fig.add_annotation(text='Potability',
                               x=0.5,y=0.5,showarrow=False,font_size=14,opacity=0.7,font_family='monospace')

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Q. How many samples of water are Potable?',x=0.47,y=0.98,
                           font=dict(color=colors_dark[2],size=20)),
                legend=dict(x=0.37,y=-0.05,orientation='h',traceorder='reversed'),
                hoverlabel=dict(bgcolor='white'))

            fig.update_traces(textposition='outside', textinfo='percent+label')

            st.plotly_chart(fig)


            # In[7]:

            st.markdown("### Total Dissolved Solids")
            st.image(Image.open("SOLIDS IN WATER.jpg"))
            st.markdown("Total dissolved solids (TDS) is a measure of the dissolved combined content of all inorganic and organic substances present in a liquid in molecular,\
             ionized, or micro-granular (colloidal sol) suspended form.\
             TDS concentrations are often reported in parts per million (ppm). Water TDS concentrations can be determined using a digital meter.")
            runvoice("Total dissolved solids (TDS) is a measure of the dissolved combined content of all inorganic and organic substances present in a liquid in molecular,\
             ionized, or micro-granular (colloidal sol) suspended form.\
             TDS concentrations are often reported in parts per million (ppm). Water TDS concentrations can be determined using a digital meter.")
            time.sleep(2)
            fig = px.histogram(df,x='TDS',y=df['TDS'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=301, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
            fig.add_vline(x=601, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
            fig.add_vline(x=901, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
            fig.add_vline(x=1201, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='<300 is considered as excellent',x=250,y=30,showarrow=False,font_size=12)
            fig.add_annotation(text='>300 and <600 is good',x=400,y=40,showarrow=False,font_size=12)
            fig.add_annotation(text='>600 and <900 is fair',x=750,y=50,showarrow=False,font_size=12)
            fig.add_annotation(text='>900 and <1200 is poor',x=1050,y=60,showarrow=False,font_size=12)
            fig.add_annotation(text='>1200 is unacceptable',x=1250,y=70,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Distribution Of Total Dissolved Solids',x=0.5,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Dissolved Solids (ppm)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[8]:

            st.markdown("### Nitrite and Nitrate")
            st.image(Image.open("no2no3.jpg"))
            st.markdown("Nitrates and nitrites are compounds that occur naturally in the human body and some foods, such as vegetables. Manufacturers also add them to processed foods, such as bacon, to preserve them and make them last longer.\
                some forms, nitrates and nitrites can be hazardous. However, they may also have health benefits.")
            runvoice("Nitrates and nitrites are compounds that occur naturally in the human body and some foods, such as vegetables. Manufacturers also add them to processed foods, such as bacon, to preserve them and make them last longer.\
            In some forms, nitrates and nitrites can be hazardous. However, they may also have health benefits.")
            time.sleep(2)    
            fig = px.histogram(df,x='NO2+NO3',y=df['NO2+NO3'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=21, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='NO2+NO3 should not exceed 20mg/L',x=20,y=75,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='NO2+NO3',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='NO2+NO3 (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[9]:

            st.markdown("### Calcium")
            st.image(Image.open("Ca.png"))
            st.markdown("Calcium is a chemical element with the symbol Ca and atomic number 20. As an alkaline earth metal, calcium is a reactive metal that forms a dark oxide-nitride layer when exposed to air.\
             Calcium is a mineral your body needs to build and maintain strong bones and to carry out many important functions. Calcium is the most abundant mineral in the body. Almost all calcium in the body is stored in bones and teeth, giving them structure and hardness.")
            runvoice("Calcium is a chemical element with the symbol Ca and atomic number 20. As an alkaline earth metal, calcium is a reactive metal that forms a dark oxide-nitride layer when exposed to air.\
             Calcium is a mineral your body needs to build and maintain strong bones and to carry out many important functions. Calcium is the most abundant mineral in the body. Almost all calcium in the body is stored in bones and teeth, giving them structure and hardness.")
            time.sleep(2)    
            fig = px.histogram(df,x='Ca',y=df['Ca'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Calcium',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Ca (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[10]:

            st.markdown("### Magnesium")
            st.image(Image.open("Magnesium.png"))
            st.markdown("Magnesium is a chemical element with the symbol Mg and atomic number 12. It is a shiny gray metal having a low density, low melting point and high chemical reactivity.\
                Magnesium is a cofactor in more than 300 enzyme systems that regulate diverse biochemical reactions in the body, including protein synthesis, muscle and nerve function, blood glucose control, and blood pressure regulation [1-3]. Magnesium is required for energy production, oxidative phosphorylation, and glycolysis.")
            runvoice("Magnesium is a chemical element with the symbol Mg and atomic number 12. It is a shiny gray metal having a low density, low melting point and high chemical reactivity.\
                Magnesium is a cofactor in more than 300 enzyme systems that regulate diverse biochemical reactions in the body, including protein synthesis, muscle and nerve function, blood glucose control, and blood pressure regulation [1-3]. Magnesium is required for energy production, oxidative phosphorylation, and glycolysis.")
            time.sleep(2)    
            fig = px.histogram(df,x='Mg',y=df['Mg'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=37.5, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='Mg should not exceed 37.5mg/L',x=38,y=75,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Magnesium',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Mg (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[11]:

            st.markdown("### Sodium")
            st.image("Na.png")
            st.markdown("Sodium is a chemical element with the symbol Na and atomic number 11. It is a soft, silvery-white, highly reactive metal. Sodium is an alkali metal, being in group 1 of the periodic table. Its only stable isotope is ²³Na. \
                It helps with the function of nerves and muscles. It also helps to keep the right balance of fluids in your body. Your kidneys control how much sodium is in your body. If you have too much and your kidneys can't get rid it, sodium builds up in your blood. This can lead to high blood pressure.")
            runvoice("Sodium is a chemical element with the symbol Na and atomic number 11. It is a soft, silvery-white, highly reactive metal. Sodium is an alkali metal, being in group 1 of the periodic table. Its only stable isotope is ²³Na. \
                It helps with the function of nerves and muscles. It also helps to keep the right balance of fluids in your body. Your kidneys control how much sodium is in your body. If you have too much and your kidneys can't get rid it, sodium builds up in your blood. This can lead to high blood pressure.")
            time.sleep(2)    
            fig = px.histogram(df,x='Na',y=df['Na'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Sodium',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Na (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[12]:

            st.markdown("### Potassium")
            st.image(Image.open("K.png"))
            st.markdown("Potassium is the chemical element with the symbol K and atomic number 19. It is a silvery white metal that is soft enough to easily cut with a knife.\
                Potassium is an essential mineral that is needed by all tissues in the body. It is sometimes referred to as an electrolyte because it carries a small electrical charge that activates various cell and nerve functions. Potassium is found naturally in many foods and as a supplement.")
            runvoice("Potassium is the chemical element with the symbol K and atomic number 19. It is a silvery white metal that is soft enough to easily cut with a knife.\
                Potassium is an essential mineral that is needed by all tissues in the body. It is sometimes referred to as an electrolyte because it carries a small electrical charge that activates various cell and nerve functions. Potassium is found naturally in many foods and as a supplement.")
            time.sleep(2)    
            fig = px.histogram(df,x='K',y=df['K'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')
            fig.update_layout(
                font_family='monospace',
                title=dict(text='Potassium',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='K (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[13]:

            st.markdown("### Chlorine")
            st.image(Image.open("Cl.png"))
            st.markdown("Chlorine is a chemical element with the symbol Cl and atomic number 17. The second-lightest of the halogens, it appears between fluorine and bromine in the periodic table and its properties are mostly intermediate between them.\
                Chlorine has a pungent, irritating odor similar to bleach that is detectable at low concentrations. The density of chlorine gas is approximately 2.5 times greater than air, which will cause it to initially remain near the ground in areas with little air movement.")
            runvoice("Chlorine is a chemical element with the symbol Cl and atomic number 17. The second-lightest of the halogens, it appears between fluorine and bromine in the periodic table and its properties are mostly intermediate between them.\
                Chlorine has a pungent, irritating odor similar to bleach that is detectable at low concentrations. The density of chlorine gas is approximately 2.5 times greater than air, which will cause it to initially remain near the ground in areas with little air movement.")
            time.sleep(2)    
            fig = px.histogram(df,x='Cl',y=df['Cl'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=251, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='Cl should not exceed 250mg/L',x=20,y=75,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Chlorine',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Cl (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[14]:
            st.markdown("### Sulphate")
            st.image(Image.open("Sulfate-ion.png"))
            st.markdown("The sulfate or sulphate ion is a polyatomic anion with the empirical formula SO2−4. Salts, acid derivatives, and peroxides of sulfate are widely used in industry. Sulfates occur widely in everyday life. Sulfates are salts of sulfuric acid and many are prepared from that acid. ")
            runvoice("The sulfate or sulphate ion is a polyatomic anion with the empirical formula SO2−4. Salts, acid derivatives, and peroxides of sulfate are widely used in industry. Sulfates occur widely in everyday life. Sulfates are salts of sulfuric acid and many are prepared from that acid. ")
            time.sleep(2)
            fig = px.histogram(df,x='SO4',y=df['SO4'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=201, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='SO4 should not exceed 250mg/L',x=20,y=75,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Sulphate',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='SO4 (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[15]:

            st.markdown("### Carbonate")
            st.image(Image.open("co3.png"))
            st.markdown("A carbonate is a salt of carbonic acid, characterized by the presence of the carbonate ion, a polyatomic ion with the formula CO2−3. The word carbonate may also refer to a carbonate ester, an organic compound containing the carbonate group C(O–)")
            runvoice("A carbonate is a salt of carbonic acid, characterized by the presence of the carbonate ion, a polyatomic ion with the formula CO2−3. The word carbonate may also refer to a carbonate ester, an organic compound containing the carbonate group C(O–)")
            time.sleep(2)    
            fig = px.histogram(df,x='CO3',y=df['CO3'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')
            fig.update_layout(
                font_family='monospace',
                title=dict(text='Carbonate',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='CO3 (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[16]:

            st.markdown("### Bi-Carbonate")
            st.image(Image.open("Bicarbonate-resonance.png"))
            st.markdown("In inorganic chemistry, bicarbonate is an intermediate form in the deprotonation of carbonic acid. It is a polyatomic anion with the chemical formula HCO⁻ ₃. Bicarbonate serves a crucial biochemical role in the physiological pH buffering system.\
                It's a byproduct of your body's metabolism. Our blood brings bicarbonate to our lungs, and then it is exhaled as carbon dioxide. Our kidneys also help regulate bicarbonate. Bicarbonate is excreted and reabsorbed by our kidneys.")
            runvoice("In inorganic chemistry, bicarbonate is an intermediate form in the deprotonation of carbonic acid. It is a polyatomic anion with the chemical formula HCO⁻ ₃. Bicarbonate serves a crucial biochemical role in the physiological pH buffering system.\
                It's a byproduct of your body's metabolism. Our blood brings bicarbonate to our lungs, and then it is exhaled as carbon dioxide. Our kidneys also help regulate bicarbonate. Bicarbonate is excreted and reabsorbed by our kidneys.")
            time.sleep(2)    
            fig = px.histogram(df,x='HCO3',y=df['HCO3'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=401, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='HCO3 should not exceed 400mg/L',x=400,y=32,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Bi-Carbonate',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='HCO3 (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[17]:

            st.markdown("### Fluorine")
            st.image(Image.open("Fluorine_Tile.png"))
            st.markdown("Fluorine is a chemical element with the symbol F and atomic number 9. It is the lightest halogen and exists at standard conditions as a highly toxic, pale yellow diatomic gas. As the most electronegative reactive element, it is extremely reactive, as it reacts with all other elements except for the light inert gases.\
                Fluorine is a nonmetallic, pale yellow-green gaseous element with a pungent odor. It is the most electronegative and reactive of all the elements. Fluorine is an element that is widely distributed in the environment, but because of its high reactivity it is not found naturally in its elemental state.")
            runvoice("Fluorine is a chemical element with the symbol F and atomic number 9. It is the lightest halogen and exists at standard conditions as a highly toxic, pale yellow diatomic gas. As the most electronegative reactive element, it is extremely reactive, as it reacts with all other elements except for the light inert gases.\
                Fluorine is a nonmetallic, pale yellow-green gaseous element with a pungent odor. It is the most electronegative and reactive of all the elements. Fluorine is an element that is widely distributed in the environment, but because of its high reactivity it is not found naturally in its elemental state.")
            time.sleep(2)    
            fig = px.histogram(df,x='F',y=df['F'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=1, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='Fluorine should not exceed 1mg/L',x=1.5,y=35,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Fluorine',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='F (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[18]:

            st.markdown("### pH Level Distribution")
            st.image(Image.open("PH_scale_3.jpg"))
            st.markdown("In chemistry, pH, also referred to as acidity, historically denoting 'potential of hydrogen', is a scale used to specify the acidity or basicity of an aqueous solution. Acidic solutions are measured to have lower pH values than basic or alkaline solutions.")
            runvoice("In chemistry, pH, also referred to as acidity, historically denoting 'potential of hydrogen', is a scale used to specify the acidity or basicity of an aqueous solution. Acidic solutions are measured to have lower pH values than basic or alkaline solutions.")
            time.sleep(2)
            fig = px.histogram(df,x='pH_GEN',y=df['pH_GEN'],color='potability',template='plotly_white',
                          marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                          barmode='group',histfunc='count')

            fig.add_vline(x=7, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='<7 is Acidic',x=4,y=70,showarrow=False,font_size=13)
            fig.add_annotation(text='>7 is Basic',x=10,y=70,showarrow=False,font_size=13)


            fig.update_layout(
                font_family='monospace',
                title=dict(text='pH Level Distribution',x=0.5,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='pH Level',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[19]:

            st.markdown("### Electrical Conductivity")
            st.image(Image.open("ec.jpg"))
            st.markdown("The conductivity of water is a measure of the capability of water to pass electrical flow. This ability directly depends on the concentration of conductive ions in the water.")
            runvoice("The conductivity of water is a measure of the capability of water to pass electrical flow. This ability directly depends on the concentration of conductive ions in the water.")
            time.sleep(2)    
            fig = px.histogram(df,x='EC_GEN',y=df['EC_GEN'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=1500, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='EC should not exceed 1500 µS/cm',x=1500,y=32,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Electrical Conductivity',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='EC (µS/cm)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[20]:

            st.markdown("### Hardness Distribution")
            st.image("hardness-of-water-1.png")
            st.markdown("Hard water is water that has high mineral content. Hard water is formed when water percolates through deposits of limestone, chalk or gypsum, which are largely made up of calcium and magnesium carbonates, bicarbonates and sulfates. Hard drinking water may have moderate health benefits. ")
            runvoice("Hard water is water that has high mineral content. Hard water is formed when water percolates through deposits of limestone, chalk or gypsum, which are largely made up of calcium and magnesium carbonates, bicarbonates and sulfates. Hard drinking water may have moderate health benefits. ")
            time.sleep(2)
            fig = px.histogram(df,x='HAR_Total',y=df['HAR_Total'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=151, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
            fig.add_vline(x=301, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)
            fig.add_vline(x=76, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='<76 mg/L is considered soft',x=75,y=30,showarrow=False,font_size=12)
            fig.add_annotation(text='Between 76 and 150 (mg/L) is moderately hard',x=120,y=40,showarrow=False,font_size=12)
            fig.add_annotation(text='Between 151 and 300 (mg/L) is considered hard',x=180,y=50,showarrow=False,font_size=12)
            fig.add_annotation(text='>300 mg/L is considered very hard',x=310,y=60,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Hardness Distribution',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Hardness (mg/L)',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[21]:

            st.markdown("### Sodium Adsorption Ratio")
            st.image(Image.open("sar.png"))
            st.markdown("Sodium adsorption ratio (SAR) means a value representing the relative amount of sodium ions to the combined amount of calcium and magnesium ions in water using the following formula: SAR = [Na]/(([Ca]+[Mg])/2)1/2, where all concentrations are expressed as milliequivalents of charge per liter.")
            runvoice("Sodium adsorption ratio (SAR) means a value representing the relative amount of sodium ions to the combined amount of calcium and magnesium ions in water using the following formula: SAR = [Na]/(([Ca]+[Mg])/2)1/2, where all concentrations are expressed as milliequivalents of charge per liter.")
            time.sleep(2)    
            fig = px.histogram(df,x='SAR',y=df['SAR'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=26, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='SAR should not exceed 26 (mmoles l−1)0.5',x=27,y=32,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Sodium Adsorption Ratio',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='SAR (mmoles l−1)0.5',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[22]:

            st.markdown("### Residual Sodium Carbonate")
            st.image(Image.open("eqn_rsc.png"))
            st.markdown("Residual sodium carbonate (RSC) is a common means of assessing the sodium permeability hazard, and takes into account the bicarbonate/carbonate and calcium/magnesium concentrations in irrigation water")
            runvoice("Residual sodium carbonate (RSC) is a common means of assessing the sodium permeability hazard, and takes into account the bicarbonate/carbonate and calcium/magnesium concentrations in irrigation water")
            time.sleep(2)    
            fig = px.histogram(df,x='RSC',y=df['RSC'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')

            fig.add_vline(x=2.5, line_width=1, line_color=colors_dark[1],line_dash='dot',opacity=0.7)

            fig.add_annotation(text='RSC should not exceed 2.5',x=2.6,y=32,showarrow=False,font_size=12)

            fig.update_layout(
                font_family='monospace',
                title=dict(text='Residual Sodium Carbonate',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='RSC',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[23]:

            st.markdown("### Percentage of Sodium Dissolved")
            st.image(Image.open("nap.png"))
            st.markdown("It says the amount of Sodium Dissolved in liquid in terms of Percentage")
            runvoice("It says the amount of Sodium Dissolved in liquid in terms of Percentage")
            time.sleep(2)    
            fig = px.histogram(df,x='Na%',y=df['Na%'],color='potability',template='plotly_white',
                              marginal='box',opacity=0.7,nbins=100,color_discrete_sequence=[colors_green[3],colors_blue[3]],
                              barmode='group',histfunc='count')
            fig.update_layout(
                font_family='monospace',
                title=dict(text='Percentage of Sodium Dissolved',x=0.53,y=0.95,
                           font=dict(color=colors_dark[2],size=20)),
                xaxis_title_text='Na%',
                yaxis_title_text='Count',
                legend=dict(x=1,y=0.96,bordercolor=colors_dark[4],borderwidth=0,tracegroupgap=5),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)


            # In[24]:


            rslt_df = df[df['potability'] == 1]


            # In[25]:


            rslt_df


            # In[26]:


            cor=df.corr()


            # In[27]:

            st.markdown("### Correlation between Variables used here")
            st.markdown("In statistics, correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data.")
            runvoice("In statistics, correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data.")
            time.sleep(2)
            fig = px.imshow(cor,height=800,width=800,color_continuous_scale=colors_blue,template='plotly_white')

            fig.update_layout(font_family='monospace',
                            title=dict(text='Correlation Heatmap',x=0.5,y=0.93,
                                         font=dict(color=colors_dark[2],size=24)),
                            coloraxis_colorbar=dict(len=0.85,x=1.1) 
                             )

            st.plotly_chart(fig, use_container_width=True)


            # In[28]:

            fig = msno.matrix(df,color=(0,0.5,0.5))


            # In[29]:


            df.isnull().sum()


            # In[30]:

            st.markdown("#### Details of Parameters which leads potability to O")
            runvoice("Details of Parameters which leads potability to O")
            time.sleep(2)    
            st.write(df[df['potability']==0].describe())


            # In[31]:

            st.markdown("#### Details of Parameters which leads potability to 1")    
            runvoice("Details of Parameters which leads potability to 1")
            time.sleep(2)    
            st.write(df[df['potability']==1].describe())


            # In[52]:


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


            if st.button('Individual Details of Well'):
                df['Date of collection'] = pd.to_datetime(df['Date of collection']).dt.strftime('%Y-%m-%d %H:%M:%S')
                # Set up Plotly figure
                well_nos = df["Well No"].unique()
                tahsils = df["Tahsil / Taluk"].unique()
                params = ["TDS", "NO2+NO3", "Ca", "Mg", "Na", "K", "Cl", "SO4", "CO3", "HCO3", "F", "pH_GEN", "EC_GEN", "HAR_Total", "SAR", "RSC", "Na%"]

                # Create the streamlit app
                st.title("Water Potability Dataset")

                # Choose the Tahsil / Taluk, Well No and parameter
                tahsil = st.selectbox("Choose a Tahsil / Taluk", tahsils)
                filtered_df = df[(df["Tahsil / Taluk"] == tahsil)]
                well_no = st.selectbox("Choose a Well No", filtered_df["Well No"].unique())
                param = st.selectbox("Choose a parameter", params)

                # Filter the dataset for the chosen Well No and parameter
                filtered_df = filtered_df[(filtered_df["Well No"] == well_no)][["Date of collection", param, "potability"]]

                # Plot the animated representation of the chosen parameter for the chosen well
                fig = px.scatter(filtered_df, x="Date of collection", y=param, color="potability", range_y=[0, filtered_df[param].max()], text=param)
                fig.update_traces(mode="markers", hovertemplate="Date: %{x}<br>Value: %{text:.2f}")
                fig.update_layout(title=f"{param} for Well No {well_no} in {tahsil}", xaxis_title="Date of collection", yaxis_title=param, showlegend=True)

                # Show the plot
                st.plotly_chart(fig)

                # Show the potability classification for the chosen well and parameter
                st.write(f"Potability of Well No {well_no} for {param}:")
                for date, potability in filtered_df[["Date of collection", "potability"]].itertuples(index=False):
                    st.write(f"- Date: {date}, Potability: {potability}")



            # In[56]:

            if st.button('Wanna Check Accuracy oF Data'):
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
                st.markdown("#### Best Algorithm for Supervised Machine Learning for our Data ")
                runvoice("Best Algorithm for Supervised Machine Learning for our Data")

                finalResults


st.markdown('''### This is the **Study App** created in Streamlit using the **pandas-profiling** library.
****Credit:**** App built in `Python` + `Streamlit` by [JASHVANTH S R ](https://www.linkedin.com/in/jashvanth-s-r-476646213)[HARUL GANESH S B ](https://www.linkedin.com/in/harul-ganesh/)[BALAJI S ](https://www.linkedin.com/in/balaji-s-csbs-dept-03790a202/)[GOWTHAM H](https://www.linkedin.com/in/gowtham-haribabu-9425861bb/)
---
''')
# In[ ]:






