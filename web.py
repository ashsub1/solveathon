import streamlit as st

# Read your HTML file
with open("index.html", "r", encoding="utf-8") as f:
    html_data = f.read()

# Embed the HTML into Streamlit
st.components.v1.html(html_data, height=1000, scrolling=True)
