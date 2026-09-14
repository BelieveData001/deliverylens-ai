import streamlit as st
import json
from google import genai
from google.genai import types

# Page settings
st.set_page_config(
    page_title="DeliveryLens AI",
    page_icon="📊",
    layout="wide"
)

# Connect to Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Page title
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
    placeholder=(
        "Example: UAT is two weeks behind schedule. "
        "Two testers are unavailable. "
        "The planned go-live date is 30 September."
    )
)

# Analyse button
if st.button("Analyse Project"):

    if not project_update.strip():
        st.warning("Please enter some project information first.")

    else:

        prompt = f"""
You are an experienced Project Manager and Delivery Manager.

Your job is to analyse project information and provide practical
delivery-management insight.

Analyse ONLY the information provided by the user.

Do not invent facts, dates, owners, budgets or project information.

If something is unknown, write:
"Information not provided."

Provide your response using the following structure:

# OVERALL PROJECT STATUS

RAG Status:
Green / Amber / Red

Status Reason:
Give a short explanation for the RAG rating.

# EXECUTIVE SUMMARY

Provide a concise summary suitable for a project sponsor or senior stakeholder.

# TOP RISKS

For each significant risk provide:

Risk:
Likelihood:
Impact:
Risk Rating:
Recommended Mitigation:
Owner:
Escalation Required: Yes / No

# KEY ISSUES

For each current issue provide:

Issue:
Impact:
Recommended Action:
Owner:
Escalation Required: Yes / No

# ACTIONS

List the most important actions.

For each action provide:

Action:
Owner:
Due Date:
Priority:

If the owner or due date is not provided, write:
"Information not provided."

# ESCALATIONS / DECISIONS REQUIRED

Identify decisions or escalations that require stakeholder or sponsor attention.

For each one provide:

Decision / Escalation:
Why it is required:
Who should decide:
Urgency:

# STAKEHOLDER UPDATE

Write a concise professional project update that a Project Manager
could send to stakeholders.

Keep the language clear, professional and concise.

PROJECT INFORMATION:

{project_update}
"""

        with st.spinner("Analysing project..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.markdown("## AI Delivery Analysis")
                st.markdown(response.text)

            except Exception as e:

                st.error("The AI request could not be completed.")
                st.write("Technical error:", str(e))
