import streamlit as st
import firebase_admin
from firebase_admin import credentials
import json

def initialize_firebase():
    # Load credentials from JSON Streamlit secrets
    cred_json = st.secrets["firebase"]["credentials"]

    # Parse string to dictionary
    cred_dict = json.loads(cred_json)

    # Initialize Firebase app if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
