import streamlit as st
import pandas as pd
import spacy

# Load the CSV data
data = pd.read_csv('chatbot_data.csv')

# Load the Spacy NLP model
nlp = spacy.load('en_core_web_sm')

# Function to check for keyword match in input text
def check_keywords(input_text):
    input_text = input_text.lower()
    for index, row in data.iterrows():
        keywords = row['keywords'].split('|')
        for keyword in keywords:
            if keyword in input_text:
                return row['responses']
    return None

# Streamlit app
def app():
    st.title("Chatbot")
    user_input = st.text_input("Enter your message:")
    if user_input:
        response = check_keywords(user_input)
        if response:
            st.text(response)
        else:
            st.text("Sorry, I couldn't understand your query.")
    else:
        st.text("Enter a message to start the conversation.")

