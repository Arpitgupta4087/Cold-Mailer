📬 Cold Mailer: AI-Powered Job Outreach Assistant

Cold Mailer is a full-stack web application designed to streamline the job application process for students and recent graduates. It leverages the power of large language models to generate personalized cold emails, scores resumes against job descriptions, and automates bulk email outreach, all through a clean and interactive Streamlit frontend.
🚀 Core Features

    📄 Smart Resume Processing: Upload your PDF resume once to power all features of the application.

    🤖 AI Cold Email Generation: Provide a job description URL or text, and the app uses a Groq-powered LLaMA 3 model to craft a compelling, personalized cold email in seconds.

    📊 Resume-JD Match Scoring: Instantly see how well your resume matches a specific job description with a score from 1-10 and a brief, AI-generated justification.

    📤 Bulk Email Automation: Upload an Excel or CSV file of recruiter contacts and send personalized emails—with your resume automatically attached—to everyone on the list.

    🔐 Secure & Private: Your API keys are kept safe in a .env file, and email automation uses secure Gmail App Passwords. No personal data is stored.

🏗️ Architecture

This project is built with a modern, decoupled architecture, ensuring scalability and separation of concerns.

    Backend (FastAPI): A robust API server built with FastAPI handles all the heavy lifting: processing resumes, making calls to the Groq LLM API, scraping web content, and calculating match scores.

    Frontend (Streamlit): A user-friendly and reactive interface built with Streamlit that communicates with the backend via HTTP requests to provide a seamless user experience.

🛠️ Tech Stack
Backend

    Python

    FastAPI: For building the robust and fast API.

    Uvicorn: As the ASGI server for FastAPI.

    LangChain: To structure and manage the LLM pipeline.

    Langchain-Groq (LLaMA 3.3): For high-speed LLM inference.

    PyMuPDF (fitz): For efficient text extraction from PDF resumes.

    BeautifulSoup4: For reliable web scraping of job descriptions.

    Pydantic: For data validation in API requests.

Frontend

    Streamlit: For the interactive web UI.

    Requests: To make API calls to the FastAPI backend.

    Pandas: For reading and processing Excel/CSV files for bulk emailing.

    smtplib: For handling the client-side email sending logic.

📝 How to Use

    Upload Resume: Start by uploading your PDF resume in the sidebar.

    Select a Feature: Choose one of the three main features from the radio buttons.

    Provide Input: Enter a job URL, paste a job description, or upload a CSV of contacts.

    Generate & Send: Click the action button to generate an email, get a match score, or send bulk emails.
