🚀 Career & Skills Advisor — Streamlit Cloud Edition

A simple and powerful Streamlit web app that recommends careers based on your skills. It analyzes your strengths, identifies missing skills, performs gap analysis, and generates a professional summary.
You can run it fully offline or enable an optional Online AI mode for enhanced summaries.

This project is designed for students, job seekers, and professionals who want a quick and personalized career direction.

🌐 Live Demo (Streamlit Cloud)

🔗 App Link:
https://your-streamlit-cloud-link-here

(Replace with your actual deployed link.)

✨ Features
🎯 Career Matching

Select your skills manually

The app matches them with popular roles such as:

Data Analyst

Data Scientist

Backend Developer

Frontend Developer

ML Engineer

Product Manager

Cybersecurity Analyst

Shows Match %, Matched Skills, Missing Skills

📊 Gap Analysis

Complete table of skill gaps

Identify what you need to learn next

Download results as CSV

🤖 Summary Generation

Two summary modes:

Mode	Description
Soft Teal (No AI)	Local template-based summary (no external API calls)
Online AI Mode	Uses an external AI provider only when you add your secret key
📄 Resume Skill Extraction

Upload PDF or DOCX resumes

Extracts skills safely and locally

No external server usage

Auto-adds detected skills to your profile

📥 Downloads

Summary (TXT)

Gap Analysis (CSV)

Saved plan from your last session

🔐 Privacy by Design

Resume content is processed in memory

App does not store or send your data anywhere

Online AI mode is opt-in

🧠 How It Works

Select Skills
Choose skills manually or upload a resume to detect skills automatically.

Matching Engine
Your skills are compared with role definitions and scored.

Gap Analysis Table
See what you’re missing for each role.

Summary Generator
Creates a career summary + 3-month development plan.

Download Reports
Get your career report as CSV and summary as TXT.

🧪 Technologies Used

Python 3.x

Streamlit

Pandas

PyPDF2

python-docx

Regex skill extraction

Streamlit Cloud for hosting

📦 Installation (Local Setup)
git clone https://github.com/burrapriyanka85-pixel/career-advisor-app.git
cd career-advisor-app

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py


Then open 👉 http://localhost:8501

☁️ Deployment on Streamlit Cloud

Push your project to GitHub

Visit https://share.streamlit.io

Click New App

Choose:

Repo: burrapriyanka85-pixel/career-advisor-app

Branch: main

File: app.py

Deploy 🎉

(Optional) Enable Online AI Mode

Add your keys in:
App → Settings → Secrets

Example:

AI_API_KEY = "your_api_key_here"
AI_PROVIDER = "openai"

📁 Project Structure
career-advisor-app/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── local/
    └── logs/

📸 Screenshots (Optional)

Create a folder docs/screenshots/ and add images like:

Home screen

Profile & Settings

Career Matches

Gap Analysis

Summary

🛠 Future Improvements

ATS resume scoring

Role-specific salary insights

Skill heatmaps

AI-generated portfolio project ideas

Company-specific role datasets

📄 License

This project is released under the MIT License.

👩‍💻 Author

Priyanka Burra
M.Sc. Bioinformatics
GitHub: https://github.com/burrapriyanka85-pixel
