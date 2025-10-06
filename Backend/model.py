import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from util import clean_text


os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0,
        )

    def extract_jobs(self, cleaned_text):
        extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = extract | self.llm
        res = chain_extract.invoke({'page': cleaned_text})
        parser = JsonOutputParser()
        res = parser.parse(res.content)
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, resume_text):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### RESUME:
            {resume_text}

            ### INSTRUCTION:
            You are a final-year student (or recent graduate) looking for an internship or entry-level opportunity.
            
            Based on the job description above and your resume, write a **cold email** to the hiring manager or company expressing your interest in the role.

            - Be polite, confident, and professional.
            - Highlight your **skills, projects, or academic work** that are most relevant to the job.
            - Mention your enthusiasm to contribute and learn.
            - Keep it concise (under 200 words), with no unnecessary preamble.
            - End with a clear call to action (e.g., open to connect, resume attached, etc.).
            - Do **not** sound like a recruiter or a company representative.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "resume_text": str(resume_text)
        })
        return res.content

    def match_score(self, job_url, resume_text):
        loader = WebBaseLoader([job_url])
        jd_text = loader.load().pop().page_content
        cleaned_jd = clean_text(jd_text)

        prompt_score = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### RESUME:
            {resume_text}

            ### INSTRUCTION:
            Rate how well the resume matches the job description on a scale of 1 to 10.
            Justify the score briefly. Return in JSON format like:
            {{
                "score": 8,
                "reason": "The candidate has relevant projects and matching skills such as Python and Flask."
            }}
            """
        )

        chain_score = prompt_score | self.llm
        res = chain_score.invoke({
            "job_description": cleaned_jd,
            "resume_text": resume_text
        })

        parser = JsonOutputParser()
        parsed = parser.parse(res.content)
        return parsed["score"], parsed["reason"]
