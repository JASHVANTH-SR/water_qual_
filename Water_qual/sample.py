import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import glob

# Load data
def app():
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
