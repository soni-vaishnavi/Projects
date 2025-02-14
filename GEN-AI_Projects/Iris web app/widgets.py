import streamlit as st
import pandas as pd
st.title("this is the text input")

name = st.text_input("enter your name")
age = st.slider("select your age :", 0,100)
st.write(f"your age is:{age}")
if name:
    st.write(f"hello, {name}")

options = ["java", "c", "python", "R"]
choice = st.selectbox("choose your language:", options)

st.write(f"you selected: {choice}")

st.write(f"{name} is {age} years old and his favourite language is {choice}")

##uploading a file

uploadfile = st.file_uploader("choose a csv file", type= "csv")



if uploadfile is not None:
    df = pd.read_csv(uploadfile)
    
    st.write(df)
    