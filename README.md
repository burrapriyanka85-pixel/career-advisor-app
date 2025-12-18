🚀 Career & Skills Advisor — Streamlit Cloud Edition

A modern, interactive Streamlit-based career guidance application that analyzes your skills, recommends suitable career paths, highlights missing skills, and generates a structured career summary with a personalized 3-month roadmap.

Designed for students, job seekers, and professionals seeking clear, data-driven career direction.

🌐 Live Application

🔗 https://career-advisor-app-hs3ebn6ftxmykronmzlp2f.streamlit.app/

✨ Features
1. Career Matching Engine

Matches your skills to popular technology roles:

Data Analyst

Data Scientist

Backend Developer

Frontend Developer

Machine Learning Engineer

Product Manager

Cybersecurity Analyst

Each recommendation includes:

Match percentage

Matched skills

Missing skills

2. Skill Gap Analysis

A complete role-by-role comparison showing:

Which skills you already have

Which skills you need to learn

A downloadable CSV report for reference

3. Two Summary Modes
Soft Teal (No AI)

Offline template-based summary

No external API calls

Fully private

Online AI Mode (Optional)

AI-enhanced career summary

Activated only when an API key is added in Streamlit Secrets

4. Resume Skill Extraction

Upload PDF or DOCX resumes

Skill extraction happens locally in memory

No data stored or uploaded

Extracted skills auto-populate your profile

5. Downloadable Reports

Career summary (TXT)

Gap analysis (CSV)

Saved career plan snapshot (per session)

6. Privacy by Design

No data is transmitted externally by default

Resume text is not saved or logged

Online AI mode is user-controlled and optional

🧠 How It Works

Select skills manually or upload a resume

The system maps your skills to predefined job role profiles

A full Gap Analysis table is generated

A career summary & 3-month roadmap is created

You can download results for later reference

🧪 Technology Stack

Python 3.x

Streamlit

Pandas

PyPDF2

python-docx

Regex-based skill parsing

Streamlit Cloud for deployment

📦 Installation (Local Setup)
git clone https://github.com/burrapriyanka85-pixel/career-advisor-app.git
cd career-advisor-app

Create a virtual environment
python -m venv venv

Activate environment

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run application
streamlit run app.py


App will run at:
👉 http://localhost:8501

☁️ Deployment on Streamlit Cloud

Push repository to GitHub

Open: https://share.streamlit.io

Click New App

Configure:

Repository: burrapriyanka85-pixel/career-advisor-app

Branch: main

File: app.py

Deploy

Enable Online AI Mode (Optional)

Add secrets in:

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

Create a folder:

docs/screenshots/


Suggested screenshots:

Home Page

Profile & Settings

Career Match Results

Skill Gap Analysis

Summary Output

🔮 Future Enhancements

ATS-based resume scoring

Salary benchmarks and job market insights

Skill heatmaps and visual analytics

AI-generated project recommendations

Organization-specific job role datasets

📄 License

Licensed under the MIT License.

👩‍💻 Author

Priyanka Burra
M.Sc. Bioinformatics
GitHub: https://github.com/burrapriyanka85-pixel
