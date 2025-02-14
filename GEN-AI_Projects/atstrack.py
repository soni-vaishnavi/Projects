from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import pdf2image
import io  # Import the io module
import base64  # Import the base64 module for encoding

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Print the API key for debugging purposes (you can remove this in production)
print(os.getenv("GOOGLE_API_KEY"))

if os.getenv("GOOGLE_API_KEY") is None:
    print("Error: GOOGLE_API_KEY is not set!")

# Function to load the GEMINI PRO MODEL and get responses
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_responses(input, pdf_content, prompt):
    response = model.generate_content(input, pdf_content[0], prompt)
    return response.text

# Function to handle PDF upload and convert to images
def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()  # Corrected this line
        first_page.save(img_byte_arr, format='PNG')  # Save image in PNG format to the byte stream
        img_byte_arr = img_byte_arr.getvalue()  # Get the byte data

        # Convert the byte data to a format usable by the Gemini model
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("File not uploaded")
