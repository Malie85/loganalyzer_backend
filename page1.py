import streamlit as st
import requests

# this is just streamlit . i dont think it needs to explain.
register_URL= "http://localhost:8000/api/register"
@st.dialog("registerForm")
def register_dialoge ():
    with st.form("Sign In"):
        realname = st.text_input("Name:")
        username = st.text_input("User name:")
        password = st.text_input("Password:", type="password")
        re_password = st.text_input("Confirm password", type="password")

        submit = st.form_submit_button("sign in")

        if submit:
            if not realname or not username or not password:
                st.warning("please fill all blanks")
            elif len(password) < 8:
                st.warning("password must be at least 8 characters")
            elif password != re_password:
                st.warning("Passwords do not match")
            else:
                payload = {
                    "realname": realname,
                    "username": username,
                    "password": password,
                    "re_password": re_password
                }

                try :
                    response= requests.post(register_URL, json=payload, timeout=10)

                    if response.status_code == 201:
                        register_response= response.json()
                        st.success(f"user {register_response['realname']} with username {register_response['username']} succesfuly registered")

                    else:
                        data = response.json()
                        if "details" in data:
                            error = data["details"][0]["message"]
                        else:
                            error = data.get("error", "unexpected error")

                        st.error(error)
        

                except requests.exceptions.ConnectionError:
                    st.error("connection failed")
                except requests.exceptions.Timeout:
                    st.error("Timedout")




if st.button("signnnn in"):
    register_dialoge()

