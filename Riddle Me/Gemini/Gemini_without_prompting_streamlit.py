from dotenv import load_dotenv
load_dotenv()  # loads all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure the Gemini API with the API key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from the Gemini LLM model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app configuration
st.set_page_config(page_title="Brain Teasers Solver ")
st.header("Solving Brain Teasers using Gemini ")
st.subheader("Made by Taufiqul Alam ")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Get user input
input = st.text_input("Input:", key="input")
submit = st.button("Ask the Brain Teaser")

# Process user input and generate a response
if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("User", input))
    
    # Show the immediate response chunk by chunk
    complete_response = ""
    for chunk in response:
        complete_response += chunk.text
    st.write(complete_response)
    
    st.session_state['chat_history'].append(("Gemini", complete_response))

# Display the chat history
st.subheader("The Chat History is ")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}", unsafe_allow_html=True)
