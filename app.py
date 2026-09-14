import streamlit as st
from google import genai

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

Analyse the project information below.

Provide the following:

1. Overall RAG status: Green, Amber or Red
2. Executive summary
3. Top 5 risks
4. Key issues requiring attention
5. Actions and owners
6. Items requiring escalation
7. Draft stakeholder update

IMPORTANT:
- Only use information provided by the user.
- Do not invent facts.
- If information is missing, say "Information not provided."
- Clearly distinguish between risks and issues.
- Keep the response concise and practical.

PROJECT INFORMATION:

{project_update}
"""

       with st.spinner("Analysing project..."):

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.markdown("## AI Delivery Analysis")
        st.markdown(response.text)

    except Exception as e:
        st.error("The AI request could not be completed.")
        st.write("Technical error:", str(e))
