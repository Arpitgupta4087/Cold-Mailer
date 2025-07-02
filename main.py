import streamlit as st
from resume import Resume
from model import Chain
from emailer import send_bulk_emails
import tempfile
from util import clean_text
from langchain_community.document_loaders import WebBaseLoader

chain = Chain()

st.set_page_config(layout="wide", page_title="AI Job Outreach", page_icon="📬")
st.title("Cold Mailer")


with st.sidebar:
    st.header("Upload Your Resume")
    uploaded_resume = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_resume:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_resume.read())
        resume_path = tmp.name


    resume_obj = Resume(resume_path)
    resume_text = resume_obj.get_text()

    st.subheader("Choose a Function")

    option = st.radio("Select a feature:", [
        "Generate Cold Email",
        "Resume-to-JD Score Matching",
        "Bulk Email Automation"
    ])

    if option == "Generate Cold Email":
        job_url = st.text_input("Enter Job URL or paste JD text:")
        if st.button("Generate Email"):
            if job_url.startswith("http"):
                loader = WebBaseLoader([job_url])
                jd = clean_text(loader.load().pop().page_content)
            else:
                jd = job_url
            email = chain.write_mail(jd, resume_text)
            st.markdown("### 🖋️ Generated Cold Email")
            st.code(email, language="markdown")


    elif option == "Resume-to-JD Score Matching":
        jd_url = st.text_input("Enter Job Description URL")
        if st.button("Get Match Score"):
            score, reason = chain.match_score(jd_url, resume_text)
            st.metric(label="Match Score", value=f"{score}/10")
            st.markdown("**Why:** " + reason)


    elif option == "Bulk Email Automation":
        st.warning("Emails will be sent from your Gmail. Use a valid App Password.")
        sender_email = st.text_input("Your Gmail Address")
        sender_password = st.text_input("Your App Password (hidden)", type="password")
        subject = st.text_input("Email Subject")
        body = st.text_area("Email Body (static for all)")
        excel_file = st.file_uploader("Upload Excel/CSV with `Email` column", type=["csv", "xlsx"])

        if st.button("Send Emails") and excel_file:
            result = send_bulk_emails(sender_email, sender_password, subject, body, excel_file,  uploaded_resume )
            if result.startswith(""):
                st.success(result)
            else:
                st.error(result)
