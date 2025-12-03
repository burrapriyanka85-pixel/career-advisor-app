# 🚀 Career & Skills Advisor — Streamlit Cloud Edition

An interactive **Streamlit-powered career recommender** that analyzes user skills, provides role recommendations, performs gap analysis, and generates a professional summary — all running securely on **Streamlit Cloud**.

This version supports **local template-based summaries**, **optional resume parsing (PDF / DOCX)**, and an **optional Online AI mode** that uses any AI API you configure through Streamlit Secrets.

---

## 🌐 Live App (Streamlit Cloud)

👉 **Live Demo:** https://your-streamlit-link-here  
*(Replace with your actual Streamlit Cloud URL)*

> 🛡️ By default, this app **does not send any data to external servers**.  
> Online AI mode works **only** if you configure your own API key inside Streamlit Secrets.

---

## ✨ Features

### 🎯 Core functionality
- **Skill → Career Matching**
- **Match % score** based on skills you have vs. role requirements
- **Gap Analysis table** (missing skills + learning roadmap)
- **Top 6 recommended roles**
- **3-month upskilling plan** auto-generated

### 📄 Resume Support (Built-in)
- Upload **PDF / DOCX** resume
- Extracts skills locally (no cloud upload)
- Automatically adds detected skills into your profile

### 🤖 Summaries (Two Modes)
| Mode | Description |
|------|-------------|
| **Local AI** (default) | Template-based writing (offline) — no external calls |
| **Online AI** (optional) | Uses an external AI provider ONLY if you add an API key in Streamlit Secrets |

### 📥 Downloads
- Export **Gap Analysis** as CSV  
- Download **Summary** as TXT  
- “Saved Plan” snapshot stored in session

### 🔒 Privacy-Focused by Design
- Resume text is parsed **locally on the server**
- **Resume content is never stored** — only filename & skill count logged
- No external API calls unless Online AI is configured

---

## 🧪 Technologies

| Technology | Purpose |
|-----------|---------|
| **Python 3.x** | Core logic |
| **Streamlit** | UI framework |
| **Pandas** | Data handling & analysis |
| **PyPDF2** | Safe PDF parsing |
| **python-docx** | DOCX parsing |
| **Streamlit Cloud** | Hosting the app |

---

## 🔧 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/burrapriyanka85-pixel/career-advisor-app.git
cd career-advisor-app

Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run app.py


App runs at:
👉 http://localhost:8501

☁️ Deploying to Streamlit Cloud (Steps)

Push your repository to GitHub

Go to: https://share.streamlit.io

Click "New App"

Select:

Repository: burrapriyanka85-pixel/career-advisor-app

Branch: main

File: app.py

Deploy

(Optional) Configure Online AI in Streamlit → Settings → Secrets

Example secrets:

AI_API_KEY = "your_key_here"
AI_PROVIDER = "openai"   # or any provider you use

📝 Project Structure
career-advisor-app/
│
├─ app.py                  # main application
├─ requirements.txt        # dependencies
├─ README.md               # documentation
├─ LICENSE                 # MIT License
├─ .gitignore              # Python ignores
└─ local/logs              # auto-created minimal logs

🧠 How It Works
1. Skills → Careers

Your skills are matched against internal job profiles such as:

Data Analyst

Data Scientist

Backend Developer

Frontend Developer

ML Engineer

Product Manager

Cybersecurity Analyst

2. Scoring
match % = (# matched skills / # required skills) * 100

3. Local Summary Generation

A summary is generated based on:

detected skills

top 3 roles

missing skills

recommended actions

4. Resume Parsing (optional)

Extracts skill keywords using regex word-boundaries

Avoids incorrect matches (e.g., “java” inside “javascript”)

No storing or transmitting of resume data

🔐 Privacy & Security

Resume files are processed in memory, not saved.

Only harmless metadata is logged (filename + skill count).

No external calls occur unless Online AI mode is enabled.

Recommended for internal/corporate use:

Protect behind login (SSO)

Host inside company VPN/VPC

Use secure secrets management

📚 Screenshots (Optional)

Create a folder: docs/screenshots/

Suggested screenshots:

Home page

Profile & Settings

Top Matches

Gap Analysis

Summary

🛠 Future Enhancements

AI-based dynamic job descriptions

ATS resume scoring

Skill gap heatmaps

Portfolio project generator

Company-specific job role integration

📄 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute with attribution.

👩‍💻 Author

Priyanka Burra
M.Sc. Bioinformatics


