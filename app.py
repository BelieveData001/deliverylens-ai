import streamlit as st

# Page settings
st.set_page_config(
    page_title="DeliveryLens AI",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("DeliveryLens AI")
st.subheader("AI-powered Project Delivery Assistant")

st.write(
    "Turn project information into delivery insights, "
    "risks, actions and escalations."
)

# Project information input
project_update = st.text_area(
    "Paste your project update below:",
    height=300,
    placeholder="Example: UAT is two weeks behind schedule..."
)

# Analyse button
if st.button("Analyse Project"):

    if not project_update.strip():
        st.warning("Please enter some project information first.")

    else:
        st.info("AI analysis will appear here.")
