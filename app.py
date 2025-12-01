# app.py
import streamlit as st
import pandas as pd
import io
import time
import html

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Career & Skills Advisor — Soft Teal (Dark Mode + AI)",
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
            {"title": "SQL for Data Science (YouTube)", "url": "https://youtube.com"}
        ],
    },
    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react"],
        "resources": [
            {"title": "FreeCodeCamp Frontend Path", "url": "https://freecodecamp.org"},
            {"title": "React Official Docs", "url": "https://react.dev"}
        ],
    },
    "Backend Developer": {
        "skills": ["python", "django", "sql", "api"],
        "resources": [
            {"title": "Django for Beginners", "url": "https://djangoproject.com"},
            {"title": "REST API Best Practices", "url": "https://restfulapi.net"}
        ],
    },
    "Machine Learning Engineer": {
        "skills": ["python", "ml", "pandas", "tensorflow"],
        "resources": [
            {"title": "Intro to ML (Coursera)", "url": "https://coursera.org"},
            {"title": "Hands-on ML (GitHub)", "url": "https://github.com/ageron/handson-ml"}
        ],
    },
    "Product Manager": {
        "skills": ["communication", "roadmapping", "analytics", "stakeholder management"],
        "resources": [
            {"title": "PM Foundations", "url": "https://coursera.org"},
            {"title": "One-page product spec guide", "url": "https://medium.com"}
        ],
    },
    "Cybersecurity Analyst": {
        "skills": ["networking", "linux", "security", "python"],
        "resources": [
            {"title": "Cybersecurity Basics", "url": "https://cybrary.it"},
            {"title": "Linux Journey (Free)", "url": "https://linuxjourney.com"}
        ],
    },
}

# ---------------- Utilities ----------------
def normalize(s: str) -> str:
    return s.strip().lower()

ALL_SKILLS = sorted({skill for v in CAREER_MAP.values() for skill in v["skills"]})

def compute_suggestions(user_skills):
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
    # safe CSS using Python triple-quote (no f-string braces problems)
    if dark_mode:
        css = """
        <style>
        /* Dark mode palette (Soft-Teal inspired) */
        .stApp { background: linear-gradient(180deg, #071418 0%, #071a1b 100%); color: #e6f7f6; font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
        .card { background: linear-gradient(180deg, rgba(10,30,30,0.85), rgba(8,22,22,0.9)); border: 1px solid rgba(255,255,255,0.04); color: #e6f7f6; border-radius:12px; padding:16px; box-shadow: 0 6px 24px rgba(0,0,0,0.6); }
        .section-header { color:#7fe3da; border-bottom:1px solid rgba(127,227,218,0.12); padding-bottom:6px; margin-bottom:12px; font-weight:700; font-size:18px; }
        .muted { color: rgba(230,247,246,0.7); }
        .pill { background: rgba(127,227,218,0.08); color:#7fe3da; padding:6px 10px; border-radius:999px; font-weight:600; margin-right:6px; display:inline-block; }
        .stButton>button { background: linear-gradient(135deg,#0fb2a1,#018f88); color:white; border-radius:10px; padding:10px 16px; border:none; font-weight:700; }
        .stDownloadButton>button { background:#0fb2a1; color:white; border-radius:10px; padding:8px 12px; }
        /* Animated fade-in for result cards */
        @keyframes fadeInUp {
            from { opacity:0; transform: translateY(12px); }
            to { opacity:1; transform: translateY(0); }
        }
        .card.animated { animation: fadeInUp 450ms ease both; }
        /* expander header style */
        .streamlit-expanderHeader { color: #7fe3da !important; font-weight:700 !important; }
        </style>
        """
    else:
        css = """
        <style>
        /* Light Soft-Teal palette */
        .stApp { background: linear-gradient(180deg, #f6fbfb 0%, #ffffff 40%, #eef7f7 100%); color: #063737; font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
        .card { background: #ffffff; border: 1px solid #dfeff0; color: #063737; border-radius:12px; padding:18px; box-shadow: 0 8px 20px rgba(3,95,98,0.06); }
        .section-header { color:#035f62; border-bottom:1px solid rgba(3,95,98,0.08); padding-bottom:6px; margin-bottom:12px; font-weight:700; font-size:18px; }
        .muted { color: #5b7a79; }
        .pill { background: rgba(15,163,165,0.08); color:#035f62; padding:6px 10px; border-radius:999px; font-weight:600; margin-right:6px; display:inline-block; }
        .stButton>button { background: linear-gradient(135deg,#0fa3a5,#0b7c7d); color:white; border-radius:10px; padding:10px 16px; border:none; font-weight:700; }
        .stDownloadButton>button { background:#0fa3a5; color:white; border-radius:10px; padding:8px 12px; }
        /* Animated fade-in for result cards */
        @keyframes fadeInUp {
            from { opacity:0; transform: translateY(12px); }
            to { opacity:1; transform: translateY(0); }
        }
        .card.animated { animation: fadeInUp 450ms ease both; }
        .streamlit-expanderHeader { color: #035f62 !important; font-weight:700 !important; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# ---------------- Sidebar controls ----------------
with st.sidebar:
    st.markdown("## Profile & Settings")
    name = st.text_input("Name (optional)")
    goal = st.selectbox("Goal", ["Explore careers", "Target a role", "Upskill for promotion"])
    selected = st.multiselect("Select your skills", options=ALL_SKILLS)
    extras = st.text_input("Extra skills (comma-separated)", help="e.g., leadership, statistics")
    st.markdown("---")

    # new features controls
    dark_mode = st.checkbox("Enable dark mode", value=False, help="Toggle dark mode for the UI")
    enable_ai = st.checkbox("Enable AI personalized text (OpenAI)", value=False)
    if enable_ai:
        st.markdown("**OpenAI settings**", unsafe_allow_html=True)
        ai_key = st.text_input("OpenAI API Key (paste here)", type="password", help="You can also configure as environment variable; this field is optional for demo.")
        model_choice = st.selectbox("Model (if available)", options=["gpt-4o-mini","gpt-4o-mini-2024","gpt-3.5-turbo"], index=2)
        ai_length = st.slider("AI response length (tokens approx.)", 64, 600, 220)

    st.markdown("---")
    include_report = st.checkbox("Enable CSV report download", value=True)
    st.caption("Tip: Provide skills above then click Suggest Careers. AI text requires API key and network access.")

# inject theme CSS based on toggle
inject_css(dark_mode)

# ---------------- Build user skills list ----------------
user_skills = [normalize(s) for s in selected]
if extras:
    for s in extras.split(","):
        if s.strip():
            user_skills.append(normalize(s))

# ---------------- Main UI ----------------
st.title("🚀 Career & Skills Advisor — Soft Teal")
st.markdown("Discover role matches and a gap analysis. Use the dark mode toggle or enable AI for a personalized narrative.")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Quick instructions")
    st.markdown("- Select your skills in the sidebar (or type extras).")
    st.markdown("- Click **Suggest Careers** to run the matching engine.")
    st.markdown("- Enable AI to generate a short personalized summary (requires OpenAI key).")
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

# store last results for export
if "last_results" not in st.session_state:
    st.session_state["last_results"] = None
if "last_profile" not in st.session_state:
    st.session_state["last_profile"] = None
if "ai_text" not in st.session_state:
    st.session_state["ai_text"] = None

if clicked:
    if not user_skills:
        st.warning("Please select or type at least one skill in the sidebar before running.")
    else:
        # animate progress a bit to feel responsive
        progress = st.progress(0)
        for p in range(0, 50, 10):
            progress.progress(p)
            time.sleep(0.02)

        results = compute_suggestions(user_skills)
        st.session_state["last_results"] = results
        st.session_state["last_profile"] = {"name": name, "goal": goal, "skills": user_skills}

        progress.progress(60)
        time.sleep(0.02)

        # Render top cards (animated)
        st.markdown("<div class='section-header'>Top Matches</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in enumerate(results[:6]):
            with cols[i % 3]:
                # add animated class when showing
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

        # Gap analysis table
        st.markdown("<div class='section-header'>Gap Analysis — Full List</div>", unsafe_allow_html=True)
        df = pd.DataFrame([{
            "Career": r["career"],
            "Match %": r["score"],
            "Matched Skills": ", ".join(r["matched"]),
            "Missing Skills": ", ".join(r["missing"])
        } for r in results])
        st.dataframe(df, use_container_width=True)

        # Save last results + provide download
        st.session_state["last_results_df"] = df
        if include_report:
            bts = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Gap Analysis (CSV)", data=bts, file_name="career_report.csv", mime="text/csv")

        progress.progress(95)
        time.sleep(0.02)

        # AI generation (optional)
        st.session_state["ai_text"] = None
        if enable_ai:
            # minimal validation
            if not (ai_key and ai_key.strip()):
                st.warning("AI is enabled but no API key provided. Paste an OpenAI API key in the sidebar to use AI features.")
            else:
                # try to import openai and call the API; fallback gracefully if anything fails
                try:
                    import openai
                    openai.api_key = ai_key.strip()
                    # prepare prompt
                    top_roles = [r["career"] for r in results[:3]]
                    prompt = f"""
You are a concise career coach. User name: {name or 'Candidate'}. Goal: {goal}.
User skills: {', '.join(user_skills)}.
Top role matches: {', '.join(top_roles)}.
For each top role, write a short (2-4 sentence) personalized guidance paragraph: why they match, 3 focused next steps to close gaps, and 2 quick learning resources (title + short URL).
Keep tone professional, encouraging, and actionable. Limit to about {ai_length} tokens.
"""
                    # show ai progress bar
                    ai_placeholder = st.empty()
                    ai_status = ai_placeholder.text("Generating personalized AI guidance...")
                    ai_progress = st.progress(0)
                    # make request
                    try:
                        # prefer Chat Completions if available; attempt compatibility
                        completion = openai.ChatCompletion.create(
                            model=model_choice,
                            messages=[{"role":"system","content":"You are a professional career coach."},
                                      {"role":"user","content": prompt}],
                            max_tokens=ai_length,
                            temperature=0.7,
                        )
                        ai_text = completion.choices[0].message.content.strip()
                    except Exception as e_chat:
                        # fallback to legacy completions if available
                        try:
                            completion = openai.Completion.create(
                                model=model_choice,
                                prompt=prompt,
                                max_tokens=ai_length,
                                temperature=0.7,
                            )
                            ai_text = completion.choices[0].text.strip()
                        except Exception as e2:
                            ai_text = f"(AI generation failed: {str(e2)})"

                    # animate fill
                    for p in range(0, 101, 25):
                        ai_progress.progress(p)
                        time.sleep(0.04)
                    ai_status.text("AI guidance ready.")
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("### Personalized AI Guidance")
                    st.write(ai_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state["ai_text"] = ai_text
                except ModuleNotFoundError:
                    st.error("`openai` library not installed. Install it in your venv (`pip install openai`) to enable AI features.")
                except Exception as e:
                    st.error(f"AI generation error: {str(e)}")
        else:
            st.info("AI personalization is disabled. Toggle 'Enable AI' in sidebar to generate a short personalized narrative using OpenAI.")
        progress.progress(100)
        time.sleep(0.01)

else:
    st.info("Select skills in the sidebar and click **Suggest Careers**. Optionally enable dark mode or AI in the sidebar.")

# ---------------- Export / last plan ----------------
st.markdown("---")
if st.session_state.get("last_results_df") is not None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Saved: Last generated plan")
    st.markdown(f"- **Name:** {html.escape(st.session_state['last_profile'].get('name','')) or '—'}")
    st.markdown(f"- **Saved skills:** {', '.join(st.session_state['last_profile'].get('skills',[])) or '—'}")
    if st.session_state.get("ai_text"):
        st.markdown("**AI summary available.**")
        st.download_button("Download AI Summary (TXT)", data=st.session_state['ai_text'].encode("utf-8"), file_name="ai_summary.txt", mime="text/plain")
    # download the saved CSV again
    csv_bytes = st.session_state["last_results_df"].to_csv(index=False).encode("utf-8")
    st.download_button("Download last plan (CSV)", data=csv_bytes, file_name="last_plan.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Professional prototype — Soft Teal edition with Dark Mode + AI personalization. AI features require an OpenAI API key and network access.")
