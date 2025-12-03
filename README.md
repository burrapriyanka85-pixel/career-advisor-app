Career & Skills Advisor — Streamlit Cloud Edition

A professional, interactive Streamlit application that recommends careers based on user skills.
The system evaluates strengths, identifies missing skills, performs role-based gap analysis, and generates a clear, structured summary along with a 3-month upskilling roadmap.

The app supports:

Soft Teal (No AI) — offline, template-based summary

Online AI Mode — optional enhanced summaries (requires API key)

Resume skill extraction (PDF / DOCX)

Secure deployment on Streamlit Cloud

This project is designed for students, job seekers, and professionals looking for personalized career guidance.

Live Demo (Streamlit Cloud)

https://career-advisor-app-hs3ebn6ftxmykronmzlp2f.streamlit.app/

Key Features
1. Career Matching Engine

Matches selected skills with common technology roles:

Data Analyst

Data Scientist

Backend Developer

Frontend Developer

Machine Learning Engineer

Product Manager

Cybersecurity Analyst

Outputs include:

Match percentage

Matched skills

Missing skills

2. Comprehensive Gap Analysis

Complete skills comparison for every supported role

Identification of missing technical and soft skills

Downloadable CSV report

3. Two Summary Modes

Soft Teal (No AI)

Default mode

Uses offline template-based summary

No external API calls

Online AI Mode (Optional)

Generates AI-based summaries

Activated only when API key is added

Fully user-controlled

4. Resume Skill Extraction

Supports PDF and DOCX resume uploads

Extracted skills are added automatically

Resume content is processed in memory

No external data storage or transmission

5. Downloadable Reports

Career summary (TXT)

Gap analysis (CSV)

Saved career plan snapshot (session-based)

6. Privacy by Design

User data is not stored or transmitted

Resume text is not logged

Online AI mode is optional and requires explicit setup

How It Works

Select skills manually or upload a resume.

The system compares your skills to predefined role profiles.

A full gap analysis is generated.

The system produces a career summary with a 3-month plan.

Reports can be downloaded for future reference.

Technology Stack

Python 3.x

Streamlit

Pandas

PyPDF2

python-docx

Regex-based skill extraction

Streamlit Cloud for hosting

Local Installation
git clone https://github.com/burrapriyanka85-pixel/career-advisor-app.git
cd career-advisor-app

Create virtual environment
python -m venv venv


Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run the application
streamlit run app.py


Access locally at:
http://localhost:8501

Deploying on Streamlit Cloud

Push your repository to GitHub

Visit: https://share.streamlit.io

Select New App

Configure:

Repository: burrapriyanka85-pixel/career-advisor-app

Branch: main

File to run: app.py

Deploy

Optional: Enable Online AI Mode

Add secrets in:

App → Settings → Secrets

Example:

AI_API_KEY = "your_api_key_here"
AI_PROVIDER = "openai"

Project Structure
career-advisor-app/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── local/
    └── logs/

Screenshots (Optional)

Create a folder:

docs/screenshots/


Suggested screenshots:

Home Page

Profile & Settings

Career Matches

Gap Analysis

Summary Section

Future Enhancements

ATS resume scoring

Salary and market insights

Skill heatmaps and visualizations

AI-generated portfolio project recommendations

Company-specific role datasets

License

This project is licensed under the MIT License.

Author

Priyanka Burra
M.Sc. Bioinformatics
GitHub: https://github.com/burrapriyanka85-pixel
