from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the updated model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load GEMINI 1.5 FLASH MODEL and get responses
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_responses(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini LLM Application")

# Text Input Section
input = st.text_input("Input: ", key="input")

# Image Upload Section
st.header("Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image and user input
if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Submit Button
submit = st.button("Submit")

# When the Submit button is clicked
if submit:
    if uploaded_file is not None:
        response = get_gemini_responses(input, image)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.warning("Please upload an image!")
