from dotenv import load_dotenv
load_dotenv()  # loads all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure the Gemini API with the API key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Few-shot examples for brain teasers
FEW_SHOT_PROMPT = """
You are an expert in solving brain teasers. Below are some examples of how to solve brain teasers.

Example 1:
Question: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?
Answer: An echo.

Example 2:
Question: The more of this you take, the more you leave behind. What is it?
Answer: Footsteps.

Example 3:
Question: What has to be broken before you can use it?
Answer: An egg.

Now solve this brain teaser:
"""

# Initialize chat history in session state
if 'chat' not in st.session_state:
    st.session_state['chat'] = model.start_chat(history=[])

# Function to get a response from the Gemini LLM model using few-shot prompting
def get_gemini_response_with_few_shot(question):
    # Add the few-shot examples to the user question
    full_prompt = FEW_SHOT_PROMPT + "\nQuestion: " + question + "\nAnswer:"
    
    # Send the question to the chat object stored in session state
    response = st.session_state['chat'].send_message(full_prompt, stream=True)
    return response

# Streamlit app configuration
st.set_page_config(page_title="Brain Teasers Solver")
st.header("Solving Brain Teasers using Gemini")
st.subheader("Made by Taufiqul Alam")

# Initialize session state for chat history display
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Get user input
input = st.text_input("Input your brain teaser:", key="input")
submit = st.button("Ask the Brain Teaser")

# Process user input and generate a response
if submit and input:
    response = get_gemini_response_with_few_shot(input)
    st.session_state['chat_history'].append(("User", input))
    
    # Show the immediate response chunk by chunk
    complete_response = ""
    for chunk in response:
        complete_response += chunk.text
    st.write(complete_response)
    
    st.session_state['chat_history'].append(("Gemini", complete_response))

# Display the chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}", unsafe_allow_html=True)
