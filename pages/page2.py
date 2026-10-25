import streamlit as st
from services.api_client import BASE_URL,get_client
import time
import requests

client = get_client()

get_user_data= client.get(f"{BASE_URL}/api/me", timeout=10)

if get_user_data.status_code != 200:
    get_user_response= get_user_data.json()
    st.write(f"Welcome {get_user_response['realname']}")
    get_user_response= get_user_data.json()
    if "details" in get_user_response:
        error = get_user_response["details"][0]["message"]
    elif "detail" in get_user_response:
        error = get_user_response["detail"]
    else:
        error = get_user_response.get("error", "unexpected error")

    st.error(error)
    time.sleep(2)
    st.switch_page("pages/page1.py")

else:
    get_user_response= get_user_data.json()
    st.write(f"Welcome {get_user_response['realname']}")
    


  
logout_URL = f"{BASE_URL}/api/logout"
if st.button("Logout"):
    try:
        response= client.post(logout_URL, timeout=10)
        data = response.json()
        if response.status_code == 200:
            logout_response= response.json()
            st.success("succesfuly logout")
            time.sleep(2)
            st.switch_page("pages/page1.py")
        


        else:
            data = response.json()
            if "details" in data:
                error = data["details"][0]["message"]
            elif "detail" in data:
                error = data["detail"]
            else:
                error = data.get("error", "unexpected error")

            st.error(error)

    except requests.exceptions.ConnectionError:
        st.error("connection failed")
    except requests.exceptions.Timeout:
            st.error("Timedout")


upload_file = st.file_uploader("upload your file",type=["log", "txt", "csv", "xml", "json"])
if upload_file is not None:
    st.success("uploaded")