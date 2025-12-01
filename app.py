# app.py
"""
Career & Skills Advisor — Soft Teal (AI and resume features removed)
- No OpenAI usage or secret handling
- No resume upload, no temporary API key sidebar
- Clean modern UI, dark-mode toggle, CSV export
Run:
    cd /path/to/project
    python -m venv venv           # create venv (if not created)
    source venv/Scripts/activate  # windows git-bash: source venv/Scripts/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    streamlit run app.py
"""
import streamlit as st
import pandas as pd
import time
import html

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Career & Skills Advisor — Soft Teal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Knowledge base ----------------
CAREER_MAP = {
    "Data Analyst": {
        "skills": ["python", "sql", "excel", "statistics"],
        "resources": [
            {"title": "Data Analysis with Python (Coursera)", "url": "https://coursera.org"},
            {"title": "SQL for Data Science (YouTube)", "url": "https://youtube.com"},
        ],
    },
    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react"],
        "resources": [
            {"title": "FreeCodeCamp Frontend Path", "url": "https://freecodecamp.org"},
            {"title": "React Official Docs", "url": "https://react.dev"},
        ],
    },
    "Backend Developer": {
        "skills": ["python", "django", "sql", "api"],
        "resources": [
            {"title": "Django for Beginners", "url": "https://djangoproject.com"},
            {"title": "REST API Best Practices", "url": "https://restfulapi.net"},
        ],
    },
    "Machine Learning Engineer": {
        "skills": ["python", "ml", "pandas", "tensorflow"],
        "resources": [
            {"title": "Intro to ML (Coursera)", "url": "https://coursera.org"},
            {"title": "Hands-on ML (GitHub)", "url": "https://github.com/ageron/handson-ml"},
        ],
    },
    "Product Manager": {
        "skills": ["communication", "roadmapping", "analytics", "stakeholder management"],
        "resources": [
            {"title": "PM Foundations", "url": "https://coursera.org"},
            {"title": "One-page product spec guide", "url": "https://medium.com"},
        ],
    },
    "Cybersecurity Analyst": {
        "skills": ["networking", "linux", "security", "python"],
        "resources": [
            {"title": "Cybersecurity Basics", "url": "https://cybrary.it"},
            {"title": "Linux Journey (Free)", "url": "https://linuxjourney.com"},
        ],
    },
}

# ---------------- Utilities ----------------
def normalize(s: str) -> str:
    return s.strip().lower()

ALL_SKILLS = sorted({skill for v in CAREER_MAP.values() for skill in v["skills"]})

def compute_suggestions(user_skills):
    """Return sorted results (highest match first)."""
    results = []
    for career, data in CAREER_MAP.items():
        req = [normalize(x) for x in data["skills"]]
        matched = sorted(list(set(user_skills) & set(req)))
        missing = sorted(list(set(req) - set(user_skills)))
        score = int(len(matched) / len(req) * 100) if req else 0
        results.append({
            "career": career,
            "score": score,
            "matched": matched,
            "missing": missing,
            "resources": data["resources"]
        })
    results = sorted(results, key=lambda r: r["score"], reverse=True)
    return results

# ---------------- Theme + CSS (light/dark + animations) ----------------
def inject_css(dark_mode: bool):
    if dark_mode:
        css = """
        <style>
        :root { --accent: #7fe3da; --muted: rgba(230,247,246,0.75); --card-bg: rgba(10,25,25,0.86); }
        html, body, .stApp { background: linear-gradient(180deg, #071418 0%, #071a1b 100%); color: #e6f7f6; font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
        .card { background: linear-gradient(180deg, rgba(10,30,30,0.85), rgba(8,22,22,0.9)); border: 1px solid rgba(255,255,255,0.04); color: #e6f7f6; border-radius:12px; padding:16px; box-shadow: 0 6px 24px rgba(0,0,0,0.6); }
        .section-header { color: var(--accent); border-bottom:1px solid rgba(127,227,218,0.12); padding-bottom:6px; margin-bottom:12px; font-weight:700; font-size:18px; }
        .muted { color: var(--muted); }
        .pill { background: rgba(127,227,218,0.08); color: #7fe3da; padding:6px 10px; border-radius:999px; font-weight:600; margin-right:6px; display:inline-block; }
        .stButton>button { background: linear-gradient(135deg,#0fb2a1,#018f88); color:white; border-radius:10px; padding:10px 16px; border:none; font-weight:700; }
        .stDownloadButton>button { background:#0fb2a1; color:white; border-radius:10px; padding:8px 12px; }
        @keyframes fadeInUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }
        .card.animated { animation: fadeInUp 450ms ease both; }
        .streamlit-expanderHeader { color: #7fe3da !important; font-weight:700 !important; }
        </style>
        """
    else:
        css = """
        <style>
        :root { --accent: #035f62; --muted: #5b7a79; --card-bg: #ffffff; }
        html, body, .stApp { background: linear-gradient(180deg, #f6fbfb 0%, #ffffff 40%, #eef7f7 100%); color: #063737; font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
        .card { background: var(--card-bg); border: 1px solid #dfeff0; color: #063737; border-radius:12px; padding:18px; box-shadow: 0 8px 20px rgba(3,95,98,0.06); }
        .section-header { color: var(--accent); border-bottom:1px solid rgba(3,95,98,0.08); padding-bottom:6px; margin-bottom:12px; font-weight:700; font-size:18px; }
        .muted { color: var(--muted); }
        .pill { background: rgba(15,163,165,0.08); color:var(--accent); padding:6px 10px; border-radius:999px; font-weight:600; margin-right:6px; display:inline-block; }
        .stButton>button { background: linear-gradient(135deg,#0fa3a5,#0b7c7d); color:white; border-radius:10px; padding:10px 16px; border:none; font-weight:700; }
        .stDownloadButton>button { background:#0fa3a5; color:white; border-radius:10px; padding:8px 12px; }
        @keyframes fadeInUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }
        .card.animated { animation: fadeInUp 450ms ease both; }
        .streamlit-expanderHeader { color: var(--accent) !important; font-weight:700 !important; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# ---------------- Sidebar controls (clean, no AI / resume) ----------------
with st.sidebar:
    st.markdown("## Profile & Settings")
    name = st.text_input("Name (optional)")
    goal = st.selectbox("Goal", ["Explore careers", "Target a role", "Upskill for promotion"])
    selected = st.multiselect("Select your skills", options=ALL_SKILLS)
    extras = st.text_input("Extra skills (comma-separated)", help="e.g., leadership, statistics")
    st.markdown("---")
    dark_mode = st.checkbox("Enable dark mode", value=False, help="Toggle dark mode for the UI")
    st.markdown("---")
    include_report = st.checkbox("Enable CSV report download", value=True)
    st.caption("Tip: Provide skills above then click Suggest Careers. This clean build does not call any external AI services.")

# Inject CSS based on dark mode toggle
inject_css(dark_mode)

# ---------------- Build user skills list ----------------
user_skills = [normalize(s) for s in selected]
if extras:
    for s in extras.split(","):
        if s.strip():
            user_skills.append(normalize(s))

# ---------------- Main UI ----------------
st.title("🚀 Career & Skills Advisor — Soft Teal")
st.markdown("Discover role matches and a gap analysis. Use the dark mode toggle in the sidebar for a different UI theme.")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Quick instructions")
    st.markdown("- Select your skills in the sidebar (or type extras).")
    st.markdown("- Click **Suggest Careers** to run the matching engine.")
    st.markdown("- Download the gap analysis as CSV if you want to save the results.")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Profile snapshot")
    st.markdown(f"- **Name:** {html.escape(name) if name else '—'}")
    st.markdown(f"- **Goal:** {goal}")
    st.markdown(f"- **Skills provided:** {len(user_skills)}")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------- Action button ----------------
clicked = st.button("🔍 Suggest Careers")

# session storage for last results
if "last_results_df" not in st.session_state:
    st.session_state["last_results_df"] = None
if "last_profile" not in st.session_state:
    st.session_state["last_profile"] = None

if clicked:
    if not user_skills:
        st.warning("Please select or type at least one skill in the sidebar before running.")
    else:
        progress = st.progress(0)
        for p in range(0, 51, 10):
            progress.progress(p)
            time.sleep(0.02)

        results = compute_suggestions(user_skills)
        st.session_state["last_profile"] = {"name": name, "goal": goal, "skills": user_skills}
        progress.progress(60)
        time.sleep(0.02)

        # Top Matches (animated cards)
        st.markdown("<div class='section-header'>Top Matches</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in enumerate(results[:6]):
            with cols[i % 3]:
                st.markdown("<div class='card animated'>", unsafe_allow_html=True)
                st.subheader(f"{r['career']} — {r['score']}%")
                st.markdown(f"**Matched:** {', '.join(r['matched']) if r['matched'] else '—'}")
                st.markdown(f"**Missing:** {', '.join(r['missing']) if r['missing'] else '—'}")
                with st.expander("Recommended resources"):
                    for res in r["resources"]:
                        st.markdown(f"- [{res['title']}]({res['url']})")
                st.markdown("</div>", unsafe_allow_html=True)

        progress.progress(80)
        time.sleep(0.02)

        # Gap analysis DataFrame
        st.markdown("<div class='section-header'>Gap Analysis — Full List</div>", unsafe_allow_html=True)
        df = pd.DataFrame([{
            "Career": r["career"],
            "Match %": r["score"],
            "Matched Skills": ", ".join(r["matched"]),
            "Missing Skills": ", ".join(r["missing"])
        } for r in results])
        st.dataframe(df, use_container_width=True)

        st.session_state["last_results_df"] = df

        if include_report:
            bts = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Gap Analysis (CSV)", data=bts, file_name="career_report.csv", mime="text/csv")

        progress.progress(100)
        time.sleep(0.02)
else:
    st.info("Select skills in the sidebar and click **Suggest Careers**. Optionally enable dark mode.")

# ---------------- Export / last plan ----------------
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
st.caption("Professional prototype — Soft Teal edition. This version does not include AI or resume upload features.")
