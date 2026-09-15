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

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )

                data = json.loads(response.text)

                st.markdown("## Project Delivery Status")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "RAG Status",
                        data.get("rag_status", "Unknown")
                    )

                with col2:
                    st.metric(
                        "Top Risks",
                        len(data.get("risks", []))
                    )

                with col3:
                    st.metric(
                        "Issues",
                        len(data.get("issues", []))
                    )

                with col4:
                    st.metric(
                        "Actions",
                        len(data.get("actions", []))
                    )
                st.markdown("## Executive Summary")

                st.write(
                    data.get(
                        "executive_summary",
                        "Information not provided."
                    )
                )
                st.markdown("## Top Risks")

                for risk in data.get("risks", []):

                    st.markdown(
                        f"**Risk:** {risk.get('risk', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Likelihood:** {risk.get('likelihood', 'Information not provided.')}  |  "
                        f"**Impact:** {risk.get('impact', 'Information not provided.')}  |  "
                        f"**Rating:** {risk.get('risk_rating', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Mitigation:** {risk.get('mitigation', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Owner:** {risk.get('owner', 'Information not provided.')}  |  "
                        f"**Escalation:** {risk.get('escalation_required', 'Information not provided.')}"
                    )

                    st.divider()
                    st.markdown("## Key Issues")

                for issue in data.get("issues", []):

                    st.markdown(
                        f"**Issue:** {issue.get('issue', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Impact:** {issue.get('impact', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Recommended Action:** {issue.get('recommended_action', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Owner:** {issue.get('owner', 'Information not provided.')}  |  "
                        f"**Escalation:** {issue.get('escalation_required', 'Information not provided.')}"
                    )

                    st.divider()
                    st.markdown("## Actions & Owners")

                for action in data.get("actions", []):

                    st.markdown(
                        f"**Action:** {action.get('action', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Owner:** {action.get('owner', 'Information not provided.')}  |  "
                        f"**Priority:** {action.get('priority', 'Information not provided.')}  |  "
                        f"**Due Date:** {action.get('due_date', 'Information not provided.')}"
                    )

                    st.divider()
                    st.markdown("## Escalations / Decisions")

                for escalation in data.get("escalations", []):

                    st.markdown(
                        f"**Decision / Escalation:** "
                        f"{escalation.get('decision_or_escalation', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Why Required:** "
                        f"{escalation.get('why_required', 'Information not provided.')}"
                    )

                    st.write(
                        f"**Decision Maker:** "
                        f"{escalation.get('who_should_decide', 'Information not provided.')}  |  "
                        f"**Urgency:** "
                        f"{escalation.get('urgency', 'Information not provided.')}"
                    )

                    st.divider()
            except Exception as e:

                st.error("The AI response could not be processed.")
                st.write("Technical error:", str(e))
