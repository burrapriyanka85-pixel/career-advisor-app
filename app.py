"""
Integrated app.py — Career & Skills Advisor
- Local template-based AI summaries (offline)
- Resume parsing (local PDF/DOCX)
- Prefill skills from resume
- CSV export, download summary, simple logs

Run:
    python -m venv venv
    venv\Scripts\activate      # Windows
    pip install -r requirements.txt
    streamlit run app.py

Requirements (requirements.txt):
streamlit
pandas
PyPDF2
python-docx
"""

import streamlit as st
import pandas as pd
import io
import os
import time
import random
import html
from typing import List, Dict

# Try imports for resume parsing
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None
try:
    import docx
except Exception:
    docx = None

# -----------------------------
# Simple career DB
# -----------------------------
CAREER_MAP = {
    "Data Analyst": {"skills": ["python","sql","excel","statistics"], "summary":"Analyze datasets, build dashboards, and support business decisions.", "level":"Entry / Mid"},
    "Data Scientist": {"skills": ["python","machine learning","statistics"], "summary":"Build ML models and experiments to solve problems.", "level":"Mid / Senior"},
    "Backend Developer": {"skills": ["python","java","apis","databases"], "summary":"Design and build backend services and APIs.", "level":"Entry / Mid"},
    "Frontend Developer": {"skills": ["html","css","javascript","react"], "summary":"Build user interfaces and client-side logic for web apps.", "level":"Entry / Mid"},
    "Machine Learning Engineer": {"skills": ["python","ml","pandas","tensorflow"], "summary":"Productionize ML models and pipelines.", "level":"Mid / Senior"},
    "Product Manager": {"skills": ["communication","roadmapping","analytics","stakeholder management"], "summary":"Drive product strategy and coordinate teams.", "level":"Entry / Mid"},
    "Cybersecurity Analyst": {"skills": ["networking","linux","security","python"], "summary":"Monitor, detect and respond to security incidents.", "level":"Entry / Mid"},
}

ALL_SKILLS = sorted({s for v in CAREER_MAP.values() for s in v["skills"]})

# -----------------------------
# Local template-based AI
# -----------------------------
LOCAL_SUMMARY_TEMPLATES = {
    "formal": [
        "Based on your skills ({skills}), a strong path is {top_careers}. To improve your match, prioritize learning {missing_top}. Suggested next steps: {steps}.",
        "You present a solid foundation in {skills}. Recommended career directions: {top_careers}. Short-term actions: {steps}."
    ],
    "friendly": [
        "Nice skillset — {skills}! Try focusing on {top_careers}. To get there faster, learn {missing_top}. Next up: {steps}.",
        "You're close — with {skills} you can target {top_careers}. Quick wins: {steps}."
    ],
    "concise": [
        "{top_careers} recommended. Fill gaps: {missing_top}. Next steps: {steps}."
    ]
}


def generate_three_month_plan(user_skills: List[str], missing_top: List[str]) -> str:
    m = [s for s in missing_top if s]
    plan_lines = [
        "3-month plan:",
        "Month 1 - Foundations: Learn core missing skill(s): " + (", ".join(m[:2]) or "review core concepts"),
        "Month 2 - Project: Build 1 small project demonstrating the skills (host on GitHub).",
        "Month 3 - Polish: Create resume bullet points, prepare 2 interview stories, apply to 5 roles/week."
    ]
    return "\n".join(plan_lines)


def local_template_summary(user_skills: List[str], ranked_results: List[Dict], style: str = "formal") -> str:
    style = style if style in LOCAL_SUMMARY_TEMPLATES else "formal"
    top = ranked_results[:3]
    top_careers = ", ".join([t["career"] for t in top]) if top else "No matches"
    # compute top missing skill across top careers
    missing = []
    for t in top:
        missing.extend(t.get("missing", []))
    missing_top = ", ".join(sorted(dict.fromkeys(missing)))[:200] or "none"
    skills_str = ", ".join(sorted(dict.fromkeys(user_skills))) or "not specified"

    # Construct recommended steps (3 bullet suggestions)
    steps = []
    lower_sk = [s.lower() for s in user_skills]
    if "python" not in lower_sk and "python" in missing_top:
        steps.append("Learn Python basics and build a small project")
    if "git" not in lower_sk:
        steps.append("Publish one project to GitHub (README + demo)")
    steps.append("Make a 1-page portfolio and prepare two interview examples")
    steps = list(dict.fromkeys(steps))[:3]
    steps_str = "; ".join(steps)

    template = random.choice(LOCAL_SUMMARY_TEMPLATES[style])
    text = template.format(skills=skills_str, top_careers=top_careers, missing_top=missing_top, steps=steps_str)
    plan = generate_three_month_plan(user_skills, missing_top.split(", ") if missing_top!="none" else [])
    return text + "\n\n" + plan

# -----------------------------
# Resume parsing (local)
# -----------------------------

def extract_text_from_pdf(file_bytes: bytes) -> str:
    if PdfReader is None:
        return ""
    txt = []
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        for p in reader.pages:
            try:
                txt.append(p.extract_text() or "")
            except Exception:
                continue
    except Exception:
        return ""
    return "\n".join(txt)


def extract_text_from_docx(file_bytes: bytes) -> str:
    if docx is None:
        return ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""


def extract_resume_text(uploaded_file) -> str:
    try:
        data = uploaded_file.read()
        uploaded_file.seek(0)
    except Exception:
        return ""
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(data)
    if name.endswith(('.doc', '.docx')):
        return extract_text_from_docx(data)
    try:
        return data.decode('utf-8', errors='ignore')
    except Exception:
        return ""


def extract_skills_from_text(text: str, skill_set: List[str]) -> List[str]:
    found = set()
    tl = text.lower()
    for s in skill_set:
        if s.lower() in tl:
            found.add(s)
    return sorted(found)

# -----------------------------
# Matching engine
# -----------------------------

def normalize(s: str) -> str:
    return s.strip().lower()


def compute_suggestions(user_skills: List[str]) -> List[Dict]:
    results = []
    uset = set([normalize(x) for x in user_skills])
    for career, data in CAREER_MAP.items():
        required = [normalize(x) for x in data["skills"]]
        matched = sorted(list(uset & set(required)))
        missing = sorted(list(set(required) - uset))
        score = int(len(matched) / len(required) * 100) if required else 0
        results.append({
            "career": career,
            "score": score,
            "matched": matched,
            "missing": missing,
            "summary": data.get("summary", ""),
            "level": data.get("level", "")
        })
    results = sorted(results, key=lambda r: r["score"], reverse=True)
    return results


def suggestions_to_df(results: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame([{
        "Career": r["career"],
        "Match %": r["score"],
        "Matched Skills": ", ".join(r["matched"]),
        "Missing Skills": ", ".join(r["missing"]),
        "Level": r.get("level", ""),
        "Summary": r.get("summary", "")
    } for r in results])
    return df

# -----------------------------
# Logs directory
# -----------------------------
LOG_DIR = os.path.join(os.getcwd(), "local", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def local_log(name: str, text: str):
    fname = os.path.join(LOG_DIR, name)
    try:
        with open(fname, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {text}\n")
    except Exception:
        pass

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Career & Skills Advisor — Local AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.card { background: linear-gradient(180deg, rgba(10,30,30,0.85), rgba(8,22,22,0.9)); border-radius:12px; padding:14px; color:#e6f7f6; margin-bottom:12px; }
.section-header { color: #7fe3da; font-weight:700; margin-bottom:10px; font-size:18px; }
.pill { background: rgba(127,227,218,0.08); color: #7fe3da; padding:6px 10px; border-radius:999px; font-weight:600; margin:2px; display:inline-block; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Profile & Settings")
    mode = st.radio("App mode", ["Soft Teal (No AI)", "Local AI (Free)"], index=1)
    st.markdown("---")
    name = st.text_input("Name (optional)")
    goal = st.selectbox("Goal", ["Explore careers", "Target a role", "Upskill for promotion"])
    selected = st.multiselect("Select your skills", options=ALL_SKILLS)
    extras = st.text_input("Extra skills (comma-separated)", help="e.g., leadership, statistics")
    st.markdown("---")
    st.markdown("Resume (optional) — local parsing only (PDF/DOCX)")
    uploaded = st.file_uploader("Upload resume (PDF / DOCX)", type=["pdf","doc","docx"], accept_multiple_files=False)
    st.markdown("---")
    style = st.selectbox("Summary style", ["formal","friendly","concise"], index=0)
    st.markdown("---")
    include_report = st.checkbox("Enable CSV report download", value=True)
    st.caption("Local AI uses template-based summaries and runs entirely offline — free and private.")

# Build skills list
user_skills = [normalize(s) for s in selected]
if extras:
    for s in extras.split(","):
        if s.strip():
            user_skills.append(normalize(s))

# If resume uploaded, parse and prefill
if uploaded is not None:
    try:
        text = extract_resume_text(uploaded)
        found = extract_skills_from_text(text, ALL_SKILLS)
        # prefill if user hasn't selected that skill already
        for f in found:
            if f not in user_skills:
                user_skills.append(f)
        st.sidebar.success(f"Parsed {uploaded.name}: found {len(found)} skills")
        local_log("resume_upload.log", f"Parsed {uploaded.name}: found {','.join(found)}")
    except Exception as e:
        st.sidebar.error(f"Resume parsing failed: {e}")

# Main UI
st.title("🚀 Career & Skills Advisor — Local Edition")
st.write("Get role suggestions, a gap analysis, and a local AI-style summary (no external API calls).")

col1, col2 = st.columns([3,1])
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Quick instructions")
    st.markdown("- Select your skills in the sidebar (or upload your resume).")
    st.markdown("- Click **Suggest Careers** to run the matching engine.")
    st.markdown("- Local AI generates a friendly summary locally (free).")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Profile snapshot")
    st.markdown(f"- **Name:** {html.escape(name) if name else '—'}")
    st.markdown(f"- **Goal:** {goal}")
    st.markdown(f"- **Skills provided:** {len(user_skills)}")
    st.markdown("</div>", unsafe_allow_html=True)

clicked = st.button("🔍 Suggest Careers")

if "last_results_df" not in st.session_state:
    st.session_state["last_results_df"] = None
    st.session_state["last_profile"] = None

if clicked:
    if not user_skills:
        st.warning("Please select or enter at least one skill in the sidebar.")
    else:
        progress = st.progress(0)
        for p in range(0,61,15):
            progress.progress(p)
            time.sleep(0.02)

        results = compute_suggestions(user_skills)
        df = suggestions_to_df(results)
        st.session_state["last_results_df"] = df
        st.session_state["last_profile"] = {"name": name, "goal": goal, "skills": user_skills}

        st.markdown("<div class='section-header'>Top Matches</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in enumerate(results[:6]):
            with cols[i % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader(f"{r['career']} — {r['score']}%")
                st.markdown(f"**Matched:** {', '.join(r['matched']) if r['matched'] else '—'}")
                st.markdown(f"**Missing:** {', '.join(r['missing']) if r['missing'] else '—'}")
                with st.expander("Recommended resources"):
                    for res in CAREER_MAP[r['career']].get("resources", []) if CAREER_MAP.get(r['career']) else []:
                        st.markdown(f"- {res}")
                st.markdown("</div>", unsafe_allow_html=True)

        progress.progress(80)
        time.sleep(0.02)

        st.markdown("<div class='section-header'>Gap Analysis — Full List</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        if include_report:
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Gap Analysis (CSV)", data=csv_bytes, file_name="career_report.csv", mime="text/csv")

        progress.progress(90)

        # Local AI summary
        if mode.startswith("Local AI"):
            st.markdown("<div class='section-header'>Local AI Summary (Free)</div>", unsafe_allow_html=True)
            summary = local_template_summary(user_skills, results, style=style)
            st.success("Local summary (generated)")
            st.write(summary)

            # Offer download of summary as text
            st.download_button("Download summary (txt)", data=summary.encode('utf-8'), file_name='career_summary.txt', mime='text/plain')
            local_log("summary.log", f"User:{name or 'anon'} Skills:{','.join(user_skills)} SummaryLen:{len(summary)}")

        progress.progress(100)
        time.sleep(0.02)
else:
    st.info("Select skills in the sidebar and click **Suggest Careers** to see recommendations.")

# Footer / saved plan
st.markdown("---")
if st.session_state.get("last_results_df") is not None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Saved: Last generated plan")
    st.markdown(f"- **Name:** {html.escape(st.session_state['last_profile'].get('name','')) or '—'}")
    st.markdown(f"- **Saved skills:** {', '.join(st.session_state['last_profile'].get('skills',[])) or '—'}")
    csv_bytes = st.session_state["last_results_df"].to_csv(index=False).encode("utf-8")
    st.download_button("Download last plan (CSV)", data=csv_bytes, file_name="last_plan.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Privacy: Uploaded resumes are parsed locally only and are not sent to external servers. Logs stored locally at 'local/logs'.")

# End of file
