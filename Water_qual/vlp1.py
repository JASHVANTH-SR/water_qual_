import streamlit as st

import os
import time
import glob


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

def app():
	colors_blue = ["#132C33", "#264D58", '#17869E', '#51C4D3', '#B4DBE9']
	colors_dark = ["#1F1F1F", "#313131", '#636363', '#AEAEAE', '#DADADA']
	colors_green = ['#01411C','#4B6F44','#4F7942','#74C365','#D0F0C0']

	new_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

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
	    st.markdown("The input dataset's first 5 rows")    
	    st.write(df.head())


	        # In[6]:

	    st.markdown("### Potability")
	    st.markdown("It defines about a liquid that is suitable for drinking or not. Parameters for drinking water quality typically fall within three categories: physical, chemical, microbiological.")
	    st.markdown("Physical and chemical parameters include heavy metals, trace organic compounds, total suspended solids, and turbidity. Chemical parameters tend to pose more of a chronic health risk through buildup of heavy metals although some components like nitrates/nitrites and arsenic can have a more immediate impact. Physical parameters affect the aesthetics and taste of the drinking water and may complicate the removal of microbial pathogens.")
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
	    st.markdown("Total dissolved solids (TDS) is a measure of the dissolved combined content of all inorganic and organic substances present in a liquid in molecular,\
	     ionized, or micro-granular (colloidal sol) suspended form.\
	     TDS concentrations are often reported in parts per million (ppm). Water TDS concentrations can be determined using a digital meter.")
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
	    st.markdown("Nitrates and nitrites are compounds that occur naturally in the human body and some foods, such as vegetables. Manufacturers also add them to processed foods, such as bacon, to preserve them and make them last longer.\
	        some forms, nitrates and nitrites can be hazardous. However, they may also have health benefits.")
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
	    st.markdown("Calcium is a chemical element with the symbol Ca and atomic number 20. As an alkaline earth metal, calcium is a reactive metal that forms a dark oxide-nitride layer when exposed to air.\
	     Calcium is a mineral your body needs to build and maintain strong bones and to carry out many important functions. Calcium is the most abundant mineral in the body. Almost all calcium in the body is stored in bones and teeth, giving them structure and hardness.")
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
	    st.markdown("Magnesium is a chemical element with the symbol Mg and atomic number 12. It is a shiny gray metal having a low density, low melting point and high chemical reactivity.\
	        Magnesium is a cofactor in more than 300 enzyme systems that regulate diverse biochemical reactions in the body, including protein synthesis, muscle and nerve function, blood glucose control, and blood pressure regulation [1-3]. Magnesium is required for energy production, oxidative phosphorylation, and glycolysis.")
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
	    st.markdown("Sodium is a chemical element with the symbol Na and atomic number 11. It is a soft, silvery-white, highly reactive metal. Sodium is an alkali metal, being in group 1 of the periodic table. Its only stable isotope is ²³Na. \
	        It helps with the function of nerves and muscles. It also helps to keep the right balance of fluids in your body. Your kidneys control how much sodium is in your body. If you have too much and your kidneys can't get rid it, sodium builds up in your blood. This can lead to high blood pressure.")
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
	    st.markdown("Potassium is the chemical element with the symbol K and atomic number 19. It is a silvery white metal that is soft enough to easily cut with a knife.\
	        Potassium is an essential mineral that is needed by all tissues in the body. It is sometimes referred to as an electrolyte because it carries a small electrical charge that activates various cell and nerve functions. Potassium is found naturally in many foods and as a supplement.")
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
	    st.markdown("Chlorine is a chemical element with the symbol Cl and atomic number 17. The second-lightest of the halogens, it appears between fluorine and bromine in the periodic table and its properties are mostly intermediate between them.\
	        Chlorine has a pungent, irritating odor similar to bleach that is detectable at low concentrations. The density of chlorine gas is approximately 2.5 times greater than air, which will cause it to initially remain near the ground in areas with little air movement.")
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
	    st.markdown("The sulfate or sulphate ion is a polyatomic anion with the empirical formula SO2−4. Salts, acid derivatives, and peroxides of sulfate are widely used in industry. Sulfates occur widely in everyday life. Sulfates are salts of sulfuric acid and many are prepared from that acid. ")
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
	    st.markdown("A carbonate is a salt of carbonic acid, characterized by the presence of the carbonate ion, a polyatomic ion with the formula CO2−3. The word carbonate may also refer to a carbonate ester, an organic compound containing the carbonate group C(O–)")
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
	    st.markdown("In inorganic chemistry, bicarbonate is an intermediate form in the deprotonation of carbonic acid. It is a polyatomic anion with the chemical formula HCO⁻ ₃. Bicarbonate serves a crucial biochemical role in the physiological pH buffering system.\
	        It's a byproduct of your body's metabolism. Our blood brings bicarbonate to our lungs, and then it is exhaled as carbon dioxide. Our kidneys also help regulate bicarbonate. Bicarbonate is excreted and reabsorbed by our kidneys.")
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
	    st.markdown("Fluorine is a chemical element with the symbol F and atomic number 9. It is the lightest halogen and exists at standard conditions as a highly toxic, pale yellow diatomic gas. As the most electronegative reactive element, it is extremely reactive, as it reacts with all other elements except for the light inert gases.\
	        Fluorine is a nonmetallic, pale yellow-green gaseous element with a pungent odor. It is the most electronegative and reactive of all the elements. Fluorine is an element that is widely distributed in the environment, but because of its high reactivity it is not found naturally in its elemental state.")
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
	    st.markdown("In chemistry, pH, also referred to as acidity, historically denoting 'potential of hydrogen', is a scale used to specify the acidity or basicity of an aqueous solution. Acidic solutions are measured to have lower pH values than basic or alkaline solutions.")
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
	    st.markdown("The conductivity of water is a measure of the capability of water to pass electrical flow. This ability directly depends on the concentration of conductive ions in the water.")
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
	    st.markdown("Hard water is water that has high mineral content. Hard water is formed when water percolates through deposits of limestone, chalk or gypsum, which are largely made up of calcium and magnesium carbonates, bicarbonates and sulfates. Hard drinking water may have moderate health benefits. ")
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
	    st.markdown("Sodium adsorption ratio (SAR) means a value representing the relative amount of sodium ions to the combined amount of calcium and magnesium ions in water using the following formula: SAR = [Na]/(([Ca]+[Mg])/2)1/2, where all concentrations are expressed as milliequivalents of charge per liter.")
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
	    st.markdown("Residual sodium carbonate (RSC) is a common means of assessing the sodium permeability hazard, and takes into account the bicarbonate/carbonate and calcium/magnesium concentrations in irrigation water")
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
	    st.markdown("It says the amount of Sodium Dissolved in liquid in terms of Percentage")
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
