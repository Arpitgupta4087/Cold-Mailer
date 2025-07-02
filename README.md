# 📬 Cold Mailer

**Cold Mailer** is an AI-powered web app that helps students and freshers generate personalized cold emails for job applications, assess resume–job fit, and even send bulk job outreach emails — all from a clean, Streamlit-based interface.

---

## 🚀 Features

- 📄 **Resume Upload**: Upload your resume (PDF) to personalize your outreach.
- 🔍 **Cold Email Generator**: Enter a job description URL or paste the JD directly, and generate a custom cold email using LLM (LLaMA 3.3 via Groq).
- 🧠 **Resume–JD Match Scoring**: Enter a JD URL and receive a relevance score and explanation based on your resume.
- 📤 **Bulk Email Automation**: Upload an Excel/CSV file with emails, and Cold Mailer will email each recipient with your uploaded resume attached.
- 🔐 **Safe & Secure**: Uses app passwords for Gmail. No data is stored.

---

## 🧪 Tech Stack

- **Python**
- **Streamlit** – UI framework
- **LangChain** + **Groq API (LLaMA 3.3)** – LLM pipeline
- **PyMuPDF (fitz)** – for resume PDF reading
- **smtplib** – for email automation
- **pandas** – for reading Excel/CSV data

