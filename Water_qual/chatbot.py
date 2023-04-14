import streamlit as st
import pandas as pd
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

# Function to check for keyword match in input text
def get_session_state():
    if 'conversations' not in st.session_state:
        st.session_state.conversations = []
    return st.session_state

def check_keywords(input_text, data):
    input_text = input_text.lower()
    for index, row in data.iterrows():
        keywords = row['keywords'].split('|')
        for keyword in keywords:
            if keyword in input_text:
                return row['responses'].strip('\"') # Remove quotes from response
    return None

# Function to perform NLP on input text using NLTK
def perform_nlp(input_text):
    tokens = nltk.word_tokenize(input_text)
    pos_tags = nltk.pos_tag(tokens)
    entities = nltk.ne_chunk(pos_tags)
    return tokens, pos_tags, entities

# Streamlit app
def app():
    st.title("Chatbot")

    # Create or get the SessionStateMixin object
    session_state = get_session_state()

    # Create or retrieve the conversation list from the SessionStateMixin
    data = pd.read_csv('chatbot_data.csv')
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

    st.text_area("Conversation:", value="\n".join(conversations), height=300)
