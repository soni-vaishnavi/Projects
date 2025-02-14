# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load all the environment variables
load_dotenv()

# Configure the Gemini model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Print the API key for debugging purposes
print(os.getenv("GOOGLE_API_KEY"))  # This should print your API key

# Check if the API key is set
if os.getenv("GOOGLE_API_KEY") is None:
    print("Error: GOOGLE_API_KEY is not set!")

# Initialize the GEMINI PRO MODEL for chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get responses from the Gemini model
def get_gemini_responses(question):
    response = chat.send_message(question, stream=True)  # Stream the response
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input text from the user
input = st.text_input("Input: ", key="input")

# Create a submit button
submit = st.button("Ask the question")

# When the response is clicked
if submit and input:
    response = get_gemini_responses(input)  # Get response from the model

    # Add user query and session history to session chat history
    st.session_state['chat_history'].append(("You", input))

    st.subheader("The response is:")
    
    # Display the streamed response in chunks
    for chunk in response:
        st.write(chunk.text)  # Write each chunk of the response
        st.session_state['chat_history'].append(("Bot", chunk.text))  # Add bot response to chat history

# Display chat history
st.subheader("The chat history is:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")  # Format and display each entry in the chat history
