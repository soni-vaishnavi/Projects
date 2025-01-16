# Importing necessary libraries for EDA
import numpy as np
import pandas as   pd
import matplotlib.pyplot as plt
import pickle
import string
import nltk
from nltk.corpus import stopwords
from flask import Flask, render_template, request
 
# Importing libraries necessary for Model Building and Training
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import   train_test_split
 
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the pre-trained model
model = tf.keras.models.load_model('Modal.keras')
x=5

# Load the tokenizer
with open('tokenizer2.pkl', 'rb') as file:
    tokenizer = pickle.load(file)
    
# Maximum sequence length used during tokenization and padding
max_len = 100

# Text preprocessing functions
def remove_subject(text):
    return text.replace('Subject', '')

def remove_punctuations(text):
    punctuations_list = string.punctuation
    temp = str.maketrans('', '', punctuations_list)
    return text.translate(temp)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    imp_words = [word.lower() for word in str(text).split() if word.lower() not in stop_words]
    return " ".join(imp_words)

# Function to preprocess user input and make predictions
def preprocess_text(user_input):
    # Apply your preprocessing functions
    user_input = remove_subject(user_input)
    user_input = remove_punctuations(user_input)
    user_input = remove_stopwords(user_input)

    # Tokenize and pad the preprocessed input
    sequences = tokenizer.texts_to_sequences([user_input])
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')

    return padded_sequences

def predict_spam_or_not_spam(user_input):
    # Preprocess the user input
    preprocessed_input = preprocess_text(user_input)

    # Make predictions
    prediction = model.predict(preprocessed_input)


    # Interpret the prediction
    if prediction[0] >= 0.5:
        return "Spam"
    else:
        return "Not Spam"


# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        user_input = request.form['user_input']
        app.logger.info(f"Received user input: {user_input}")
        result = predict_spam_or_not_spam(user_input)
        app.logger.info(f"Prediction result: {result}")
        return render_template('index.html', result=result, user_input=user_input)
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
