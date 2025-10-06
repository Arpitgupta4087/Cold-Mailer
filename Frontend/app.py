import streamlit as st
import requests
import pandas as pd
from emailer import send_bulk_emails # This is now a local import in the frontend folder

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"
st.set_page_config(layout="wide", page_title="AI Job Outreach", page_icon="📬")
st.title("AI Job Outreach Assistant")


# --- Helper function to process resume via API ---
def process_resume(uploaded_file):
    """Sends resume to backend for processing and stores text in session state."""
    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try:
        with st.spinner("Processing your resume..."):
            response = requests.post(f"{BACKEND_URL}/process-resume/", files=files)
            if response.status_code == 200:
                st.session_state.resume_text = response.json().get("resume_text")
                st.success("Resume processed successfully!")
            else:
                st.error(f"Error processing resume: {response.text}")
                st.session_state.resume_text = None
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        st.session_state.resume_text = None


# --- Sidebar for Resume Upload ---
with st.sidebar:
    st.header("1. Upload Your Resume")
    uploaded_resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

    if uploaded_resume:
        if "resume_text" not in st.session_state or st.session_state.get("resume_filename") != uploaded_resume.name:
            process_resume(uploaded_resume)
            st.session_state.resume_filename = uploaded_resume.name

# --- Main Application Logic ---
if "resume_text" in st.session_state and st.session_state.resume_text:
    st.info("Resume loaded. You can now use the features below.")

    option = st.radio("Select a feature:", [
        "Generate Cold Email",
        "Resume-to-JD Score Matching",
        "Bulk Email Automation"
    ], key="feature_select")

    # --- Feature 1: Generate Cold Email ---
    if option == "Generate Cold Email":
        st.subheader("✉️ Generate Cold Email")
        job_url_or_text = st.text_area("Paste the job description URL or text here:")
        
        if st.button("Generate Email"):
            if not job_url_or_text:
                st.warning("Please provide a job description or URL.")
            else:
                payload = {
                    "job_description": job_url_or_text, # Backend can handle URL or text
                    "resume_text": st.session_state.resume_text
                }
                try:
                    with st.spinner("Crafting your email..."):
                        response = requests.post(f"{BACKEND_URL}/generate-email/", json=payload)
                        if response.status_code == 200:
                            email = response.json().get("email")
                            st.markdown("### 🖋️ Generated Cold Email")
                            st.code(email, language="markdown")
                        else:
                            st.error(f"Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the backend: {e}")

    # --- Feature 2: Resume-to-JD Score Matching ---
    elif option == "Resume-to-JD Score Matching":
        st.subheader("📊 Resume-to-JD Score Matching")
        jd_url = st.text_input("Enter the Job Description URL:")

        if st.button("Get Match Score"):
            if not jd_url:
                st.warning("Please enter a job URL.")
            else:
                payload = {
                    "job_url": jd_url,
                    "resume_text": st.session_state.resume_text
                }
                try:
                    with st.spinner("Analyzing match..."):
                        response = requests.post(f"{BACKEND_URL}/match-score/", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            score = data.get("score")
                            reason = data.get("reason")
                            st.metric(label="Match Score", value=f"{score}/10")
                            st.markdown(f"**Justification:** {reason}")
                        else:
                            st.error(f"Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the backend: {e}")
                    
    # --- Feature 3: Bulk Email Automation ---
    elif option == "Bulk Email Automation":
        st.subheader("🚀 Bulk Email Automation")
        st.warning("This feature sends emails directly from this browser session. Ensure your Gmail App Password is correct.")
        
        with st.form("bulk_email_form"):
            sender_email = st.text_input("Your Gmail Address")
            sender_password = st.text_input("Your App Password", type="password")
            subject = st.text_input("Email Subject")
            body = st.text_area("Email Body (this will be sent to all recipients)")
            excel_file = st.file_uploader("Upload Excel/CSV with an 'Email' column", type=["csv", "xlsx"])
            
            submitted = st.form_submit_button("Send Emails")

            if submitted:
                if not all([sender_email, sender_password, subject, body, excel_file]):
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Sending emails..."):
                        # Note: 'uploaded_resume' is the file-like object from the initial upload
                        result = send_bulk_emails(sender_email, sender_password, subject, body, excel_file, uploaded_resume)
                        if "✅" in result:
                            st.success(result)
                        else:
                            st.error(result)
else:
    st.warning("Please upload your resume in the sidebar to begin.")