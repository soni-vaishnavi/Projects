from dotenv import load_dotenv
load_dotenv()
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
#used for interacting with os
import os
import sqlite3 #uesd to intearct with sqlite database
import google.generativeai as genai #for accessing google gemini model..to convert NLP to SQL

#CODE Given below is to configure api

# Configure our API Key
genai.configure(api_key='AIzaSyAqoe7c-D8-bDpwgkF8y9Y0l2hiUai4_fE')


#to understand this code we must know the concept of function

##    IMP     ##
#CPNY QUSTN ON FUNCTN: Purpose of function? what is the difference in deep and shalow copy?
# how can you pass parameter in function?
#what are decorator in python?
# how can you implement function caching in python
# Function to load Gemini Model and Provide Query as Response


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from SQL Database
def read_sql_query(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

# Prompt for the Gemini model
prompt = [
    """
    You are an expert in translating English questions into SQL queries based on a database called STUDENT, 
    which has the following columns: NAME, CLASS, SECTION, and MARKS.
    
    Follow these instructions carefully:
    - When asked to create an SQL query, write only the SQL command as a single string without using backticks (```) or mentioning the word "SQL".
    - Ensure there are no unnecessary spaces or newline characters in the output.
    - For example:
      - Example 1: "How many entries of records are present?" should be translated to:
        SELECT COUNT(*) FROM STUDENT;
      - Example 2: "Tell me all the students studying in the Data Science class?" should be translated to:
        SELECT * FROM STUDENT WHERE CLASS = 'Data Science';
      - Example 3: "Insert a new student named Yash in Class FSD, Section J with 99 marks." should be translated to:
        INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Yash', 'FSD', 'J', 99);
    
    If the question involves generating a graph, respond with a single string in the following format:
    SQL query,graph type,column whose graph is needed
    - For example:
      - "Generate a bar graph of all student marks." should be translated to:
        SELECT MARKS FROM STUDENT;|bar|MARKS
    - Make sure the graph type and column name match the question accurately, and ensure there are no newline characters in the response.
    
    Ensure the output is precise, formatted as a single string, and does not include unnecessary elements like lists or additional characters. All SQL commands should be clear, concise, and free from extraneous spaces.
    """
]

# Streamlit App Configuration
st.set_page_config(page_title='Retrieve SQL Query from Natural Language')
st.header("Gemini App To Retrieve SQL Data")

# Input from the user
question = st.text_input("Input: ", key="input")

# Button for submitting the question
submit = st.button("Ask the question")

# Retrieve student names from the database
student_name = read_sql_query("SELECT NAME FROM STUDENT", "student.db")
student_name_list = [item[0] for item in student_name]
print(student_name_list)

# If the submit button is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    
    # Splitting the response to separate SQL query and graph type
    ls = response.split('|')
    print(ls)
    
    # Extract the SQL query from the response
    query = ls[0].strip()
    print(query)
    
    # Execute the SQL query to get the result
    response = read_sql_query(query, "student.db")
    st.subheader("The Response is")
    
    # Extract the query result into a list for display
    response_lst = [item[0] for item in response]
    print(response_lst)
    st.header(response_lst)

    # Handling the graph based on the second part of the response (graph type)
    try:
        if ls[1].strip() == 'bar':
            # Prepare data for the bar chart
            data = {"Student Index": student_name_list, "Marks": response_lst}
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index("Student Index"))

        elif ls[1].strip() == 'pie':
            # Prepare the pie chart data
            data = {"Student Index": student_name_list, "Marks": response_lst}
            df = pd.DataFrame(data)
            plt.figure(figsize=(8, 6))
            plt.pie(df['Marks'], labels=df['Student Index'], autopct='%1.1f%%', startangle=140)
            plt.title('Marks Distribution by Student')
            st.pyplot(plt)  # Display the pie chart

    except Exception as e:
        print(e)
