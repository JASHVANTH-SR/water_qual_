import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Load data
def app():
    translator = Translator()

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

    @st.cache(allow_output_mutation=True,suppress_st_warning=True)
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
