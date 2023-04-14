import streamlit as st
import pandas as pd
import spacy

# Load the Spacy NLP model
nlp = spacy.load('en_core_web_sm')

# Function to check for keyword match in input text
def check_keywords(input_text, data):
    input_text = input_text.lower()
    for index, row in data.iterrows():
        keywords = row['keywords'].split('|')
        for keyword in keywords:
            if keyword in input_text:
                return row['responses']
    return None

# Function to perform NLP on input text
def perform_nlp(input_text):
    doc = nlp(input_text)
    tokens = [token.text for token in doc]
    pos_tags = [token.pos_ for token in doc]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return tokens, pos_tags, entities

# Streamlit app
def app():
    st.title("Chatbot")

    # Create or get the SessionStateMixin object
    session_state = get_session_state()

    # Create or retrieve the conversation list from the SessionStateMixin
    if 'conversations' not in session_state:
        session_state.conversations = []
    conversations = session_state.conversations

    user_input = st.text_input("You:")

    if user_input:
        conversations.append("You: " + user_input)
        response = check_keywords(user_input, data)
        if response:
            conversations.append("Bot: " + response)
        else:
            conversations.append("Bot: Sorry, I couldn't understand your query.")
            tokens, pos_tags, entities = perform_nlp(user_input)
            st.write("Tokens: ", tokens)
            st.write("POS Tags: ", pos_tags)
            st.write("Entities: ", entities)

    st.text_area("Conversation:", value="\n".join(conversations), height=300)

# Function to create or retrieve the SessionStateMixin object
    def get_session_state():
        return st.session_state

    # Load the CSV data
    data = pd.read_csv('chatbot_data.csv')

