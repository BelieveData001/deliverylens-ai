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

Analyse ONLY the project information provided by the user.

Do not invent facts, dates, owners, budgets or project information.

If information is missing, use:
"Information not provided."

Return ONLY valid JSON.

Use exactly this structure:

{{
  "rag_status": "Green / Amber / Red",
  "status_reason": "Short explanation for the RAG rating.",

  "executive_summary": "Concise summary suitable for a project sponsor or senior stakeholder.",

  "risks": [
    {{
      "risk": "Risk description",
      "likelihood": "Low / Medium / High",
      "impact": "Low / Medium / High",
      "risk_rating": "Low / Medium / High",
      "mitigation": "Recommended mitigation",
      "owner": "Owner or Information not provided",
      "escalation_required": "Yes / No"
    }}
  ],

  "issues": [
    {{
      "issue": "Current issue",
      "impact": "Impact of the issue",
      "recommended_action": "Recommended action",
      "owner": "Owner or Information not provided",
      "escalation_required": "Yes / No"
    }}
  ],

  "actions": [
    {{
      "action": "Action required",
      "owner": "Owner or Information not provided",
      "due_date": "Due date or Information not provided",
      "priority": "High / Medium / Low"
    }}
  ],

  "escalations": [
    {{
      "decision_or_escalation": "Decision or escalation required",
      "why_required": "Why stakeholder or sponsor attention is required",
      "who_should_decide": "Decision maker or Information not provided",
      "urgency": "High / Medium / Low"
    }}
  ],

  "stakeholder_update": "Concise professional project update suitable for sending to stakeholders."
}}

PROJECT INFORMATION:

{project_update}
"""
             with st.spinner("Analysing project..."):

    try:

        response = None

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )

                break

            except Exception as api_error:

                if "503" in str(api_error) and attempt < 2:

                    import time
                    time.sleep(5)

                else:

                    raise api_error

        st.markdown("## AI Delivery Analysis")
        st.markdown(response.text)

    except Exception as e:

        st.error("The AI request could not be completed.")
        st.write("Technical error:", str(e))
