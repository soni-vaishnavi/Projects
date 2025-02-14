import streamlit as st
import pandas  as pd
import numpy as np

#title of the  application

st.title("hello streamlit")

#display a simple text

st.write("this is a simple text")

#create a simple dataframe


df = pd.DataFrame({'first column': [1,2,3,4],   'second column': [10, 20,30, 40]})

##display the dataframe


st.write("here is the dataframe", df)

#create a line chart

chartdata = pd.DataFrame(   np.random.randn(20,3), columns=['a', 'b', 'c'])
st.line_chart(chartdata)
