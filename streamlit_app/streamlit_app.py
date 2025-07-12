# streamlit_app/app.py

import streamlit as st
import pandas as pd
import pickle
import os

# Load the model and vectorizer
@st.cache_resource
def load_model():
    model_path = "../models/model.pkl"
    vectorizer_path = "../models/vectorizer.pkl"
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    else:
        st.error("Model or vectorizer not found!")
        return None, None

model, vectorizer = load_model()

# Streamlit UI
st.set_page_config(page_title="CBTC Log Analyzer", layout="wide")
st.title("🚆 CBTC Log Analyzer - Fault Classifier")
st.markdown("Enter a CBTC log message below to classify the fault type:")

# Text input
log_input = st.text_area("Log Message", placeholder="e.g. Lost communication with train ID 241")

# Predict button
if st.button("🔍 Classify Fault Type"):
    if not log_input.strip():
        st.warning("Please enter a log message.")
    else:
        vector = vectorizer.transform([log_input])
        prediction = model.predict(vector)[0]
        st.success(f"🛠️ Predicted Fault Type: **{prediction}**")
