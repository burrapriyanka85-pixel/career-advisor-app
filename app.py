# app.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Generative AI for Youth — Career Guidance", layout="centered")

st.title("Generative AI for Youth Mental Wellness — Career Guidance")
st.markdown("Confidential, empathetic career guidance based on your technical knowledge.")

with st.form(key="career_form"):
    skills = st.text_area(
        "List your technical skills / tools / languages",
        placeholder="e.g. Python, SQL, Pandas, Scikit-learn, Bioinformatics tools, FHIR, Power BI",
        height=120,
    )
    education = st.selectbox("Education level", ["High School", "Undergraduate", "Postgraduate", "Professional / Bootcamp", "Other"])
    interests = st.text_input("Your interests (e.g., data, biology, apps, security)", placeholder="e.g. Data Science, Bioinformatics, Healthcare Analytics")
    submit = st.form_submit_button("Get guidance")

def suggest_careers(skills_text, interests_text, education_level):
    # normalize inputs
    s = skills_text.lower()
    i = interests_text.lower()
    suggestions = []
    reasons = []
    next_steps = []

    # Ruleset: look for keywords
    if any(keyword in s for keyword in ["python", "pandas", "numpy", "scikit", "sklearn", "matplotlib", "seaborn"]):
        suggestions.append("Data Analyst")
        reasons.append("You already have strong Python data-analysis tools.")
        next_steps.append("Practice exploratory data analysis (EDA), SQL, and dashboarding (Power BI / Tableau).")

    if any(keyword in s for keyword in ["scikit", "sklearn", "tensorflow", "pytorch", "keras", "machine learning", "ml"] ) or "machine learning" in i:
        suggestions.append("Machine Learning Engineer / ML Researcher")
        reasons.append("You have machine learning libraries and model-building experience.")
        next_steps.append("Learn model deployment (FastAPI, Docker), and practice deep learning frameworks (TensorFlow/PyTorch).")

    if any(keyword in s for keyword in ["java", "spring", "api", "fastapi", "flask", "backend"]):
        suggestions.append("Backend Developer / API Engineer")
        reasons.append("You have backend / API-relevant skills.")
        next_steps.append("Focus on RESTful API design, databases, and cloud deployment.")

    if any(keyword in s for keyword in ["blast", "bowtie2", "fastqc", "bioinformatics", "genomics", "sequencing"] ) or "bio" in i:
        suggestions.append("Bioinformatics Data Scientist / Computational Biologist")
        reasons.append("Your bioinformatics tools and interests line up with computational biology roles.")
        next_steps.append("Work on genomics analysis projects, learn Bioconductor or BioPython, and publish reproducible notebooks.")

    if "health" in i or "healthcare" in i or any(k in s for k in ["fhir", "hipaa"]):
        suggestions.append("Healthcare Data Engineer / Clinical Data Analyst")
        reasons.append("Your knowledge of FHIR/HIPAA and healthcare domain is valuable for clinical data roles.")
        next_steps.append("Study healthcare data standards (FHIR), data governance, and privacy-compliant pipelines.")

    # fallback / general suggestions
    if not suggestions:
        suggestions = ["Data Analyst", "Software Developer", "Technical Research Assistant"]
        reasons = ["These are good starter roles that use common skills like Python and data tooling."] * len(suggestions)
        next_steps = [
            "Build small projects using pandas and scikit-learn; create a GitHub portfolio.",
            "Learn a web framework (Flask/FastAPI) and practice building REST APIs.",
            "Look for research internships; get comfortable with reproducible analyses."
        ]

    # tailor by education
    edu_msg = ""
    if education_level == "High School":
        edu_msg = "Since you're at High School level, focus on learning fundamentals: Python, basic statistics, and small projects."
    elif education_level == "Undergraduate":
        edu_msg = "As an undergraduate, aim for internships and projects; publish notebooks and learn tools like SQL and Git."
    elif education_level == "Postgraduate":
        edu_msg = "As a postgraduate, highlight research, thesis work, and deployable projects; consider specialized roles."
    else:
        edu_msg = "Focus on practical projects and certifications to strengthen job applications."

    return suggestions, reasons, next_steps, edu_msg

if submit:
    if not skills.strip() and not interests.strip():
        st.warning("Please add at least some skills or interests so I can give helpful guidance.")
    else:
        suggestions, reasons, next_steps, edu_msg = suggest_careers(skills, interests, education)
        st.subheader("Suggestions:")
        for idx, job in enumerate(suggestions):
            st.markdown(f"**{idx+1}. {job}**")
            st.markdown(f"- Why: {reasons[idx]}")
            st.markdown(f"- First steps: {next_steps[idx]}")
        st.markdown("---")
        st.info(edu_msg)

        # offer detailed plan for top suggestion
        st.subheader("Detailed plan for top suggestion")
        top = suggestions[0]
        if top.lower().startswith("data analyst"):
            plan = dedent("""
            1. Projects: 3 small projects (EDA + visualization + basic model).
            2. Skills: Pandas, SQL, Excel, Power BI, storytelling.
            3. Apply: internships, Kaggle, volunteer for research data cleaning.
            4. Portfolio: GitHub README with instructions, and a short demo GIF.
            """)
        elif "machine learning" in top.lower() or "ml" in top.lower():
            plan = dedent("""
            1. Projects: classification/regression projects, include model explainability.
            2. Skills: Scikit-learn, TensorFlow/PyTorch, model deployment (FastAPI/Docker).
            3. Apply: ML internships, ML engineer roles; contribute to open-source.
            4. Portfolio: a deployed demo and a notebook with reproducible results.
            """)
        elif "bioinformatics" in top.lower() or "computational" in top.lower():
            plan = dedent("""
            1. Projects: genome analysis, variant calling, RNA-seq pipelines.
            2. Skills: BioPython, Bioconductor, command-line NGS tools, Nextflow/Snakemake.
            3. Apply: research assistant roles, internships in computational biology labs.
            4. Portfolio: reproducible pipelines and well-documented notebooks.
            """)
        else:
            plan = "Build relevant small projects, document them on GitHub, and start applying to internships."

        st.write(plan)

        # Helpful links (editable)
        st.markdown("**Resources to get started:**")
        st.markdown("- FreeCodeCamp / Coursera / edX for structured courses")
        st.markdown("- Kaggle competitions and datasets")
        st.markdown("- Streamlit for small demos; FastAPI for deployment; GitHub for portfolio")
        st.markdown("---")
        st.write("If you'd like, paste your GitHub profile link and I can suggest which projects to pin or improve.")
