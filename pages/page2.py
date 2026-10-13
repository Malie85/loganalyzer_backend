import streamlit as st
import requests
from services.api_client import BASE_URL,get_client

client = get_client()

get_user_data= client.get(f"{BASE_URL}/api/me", timeout=10)

if get_user_data.status_code == 200:
    get_user_response= get_user_data.json()
    st.write(f"Welcome {get_user_response['realname']}")
    
