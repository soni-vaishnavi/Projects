from dotenv import load_dotenv
load_dotenv()  ##loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))



print(os.getenv("GOOGLE_API_KEY"))  # This should print your API key

if os.getenv("GOOGLE_API_KEY") is None:
    print("Error: GOOGLE_API_KEY is not set!")

##funtion to load GEMINI PRO MODEL and get responses
model = genai.GenerativeModel("gemini-pro")
def get_gemini_responses(question):
    response = model.generate_content(question)
    return response.text


# initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

input = st.text_input("Input: ", key="input")

submit = st.button("ask the question")

# when response is clicked

if submit:
    response = get_gemini_responses(input)
    st.subheader("the response is:")
    st.write(response)


