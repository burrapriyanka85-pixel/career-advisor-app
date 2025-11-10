# 🚀 Personalized Career & Skills Advisor

An interactive **Streamlit web app** that suggests personalized career paths based on your skills, goals, and uploaded resumes.

This project is designed to assist students and professionals in discovering potential career paths based on their technical skills, interests, and education level. It provides a personalized skill–career match analysis and suggests learning resources to bridge knowledge gaps.

---

## 🌟 Features

✅ **Skill-based career recommendations** — get personalized career suggestions based on your listed skills  
✅ **Gap analysis** — see which skills you have vs. which are missing for specific career paths  
✅ **Resource links** — curated online courses, tutorials, and learning materials  
✅ **Optional resume skill extraction** (upload `.txt` or `.pdf` in future version)  
✅ **Add custom careers during session**  
✅ **Download results** — export your gap analysis as `.csv` or `.xlsx`  
✅ **Built with** `Streamlit` **and** `pandas`

---

## 🧠 How It Works

1. You input your technical skills (e.g., Python, SQL, Excel, HTML, etc.)  
2. The system compares your skills with predefined skill sets from popular job roles  
3. It calculates a **match score (%)** and identifies **missing skills**  
4. It displays personalized learning resources to help you upskill  
5. You can download a full report as a `.csv` file  

---

## 🧩 Technologies Used

| Technology | Purpose |
|-------------|----------|
| **Python** | Core programming language |
| **Streamlit** | Web app framework |
| **Pandas** | Data analysis and DataFrame handling |
| **GitHub** | Version control and hosting |
| **Markdown** | Documentation formatting |

---

## 🧠 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/burrapriyanka85-pixel/career-advisor-app.git
cd career-advisor-app

2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app.py
Then open your browser and go to 👉 http://localhost:8501

👩‍💻 Author
Priyanka Burra
🎓 Final Year M.Sc. Bioinformatics Project
💡 Built using Python, Streamlit, and Pandas for data-driven career guidance and analytics.

📜 License
This project is open-source and available under the MIT License
You can freely use, modify, and distribute this code with attribution.

🎯 Future Enhancements
Resume parsing (PDF skill extraction)
AI-based dynamic job suggestions
Integration with LinkedIn APIs
Personalized upskilling plan generation
