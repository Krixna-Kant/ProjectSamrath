import streamlit as st
from src.qa_engine import get_rainfall_response

st.set_page_config(page_title="Rainfall Insight", page_icon="🌦️")

st.title("🌧️ Rainfall Data Analysis - IMD 2017")

st.markdown("""
Enter a **State or Subdivision Name** (e.g. *Karnataka*, *Andaman and Nicobar Islands*, *Konkan & Goa*)  
and get the average annual rainfall.
""")

user_input = st.text_input("Enter State/Subdivision:", "")

if st.button("Get Rainfall"):
    if user_input.strip():
        with st.spinner("Fetching data..."):
            result = get_rainfall_response(user_input)
        st.success(result)
    else:
        st.warning("Please enter a valid name.")
