import streamlit as st

page1 = st.Page("pages/page1.py", title="Login")
page2 = st.Page("pages/page2.py", title="Welcome")

pg = st.navigation([page1, page2], position="hidden")
pg.run()