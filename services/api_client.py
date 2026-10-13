import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_client():
    if "api_client" not in st.session_state:
        st.session_state.api_client = requests.Session()

    return st.session_state.api_client