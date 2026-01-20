import streamlit as st
import os
import sqlite3
from datetime import datetime
from config import PROFILE

st.set_page_config(
    page_title="Job Application Toolkit",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    /* Step indicator styling */
    .step-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }
    .step-complete {
        background: #10B981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(103, 126, 234, 0.1);
        border: 1px solid rgba(103, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Skill badges */
    .skill-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    /* Transferable skill styling */
    .transfer-badge {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    /* Hide default Streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
defaults = {
    "step": 1,
    "job_content": None,
    "matched_skills": [],
    "transferable_skills": [],  
    "job_info": {"company": "", "title": "", "location": "", "url": ""},
    "cover_letter": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Load .env
from dotenv import load_dotenv
load_dotenv()

cerebras_key = os.getenv("CEREBRAS_API_KEY", "")
voyage_key = os.getenv("VOYAGE_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY", "")
jina_key = os.getenv("JINA_API_KEY", "")

# Initialize Cerebras
cerebras_client = None
if cerebras_key:
    try:
        from cerebras.cloud.sdk import Cerebras
        cerebras_client = Cerebras(api_key=cerebras_key)
    except Exception as e:
        pass

# Database - simplified schema
def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            company TEXT,
            title TEXT,
            location TEXT,
            url TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn

conn = init_db()

with st.sidebar:
    st.title("⚙️ API Status")
    st.success("✅ Cerebras" if cerebras_key else "❌ Cerebras")
    st.success("✅ Tavily" if tavily_key else "⚪ Tavily")
    st.success("✅ Voyage" if voyage_key else "⚪ Voyage")
    st.success("✅ Jina" if jina_key else "⚪ Jina")
    
    # CV Matching Scores (if job analyzed)
    if st.session_state.get("cv_scores"):
        st.markdown("---")
        st.markdown("### 📄 Resume Match Scores")
        for profile_key, score_data in st.session_state.cv_scores:
            score = score_data["score"]
            name = score_data["profile_name"]
            if profile_key == st.session_state.get("best_cv"):
                st.markdown(f"🏆 **{name}**: {score}%")
            else:
                st.markdown(f"📄 {name}: {score}%")
    
    st.markdown("---")
    st.markdown("### 📁 Recent Applications")
    c = conn.cursor()
    c.execute("SELECT company, title, status FROM applications ORDER BY created_at DESC LIMIT 5")
    for job in c.fetchall():
        emoji = {"Applied": "📤", "Saved": "📌"}.get(job[2], "📋")
        st.markdown(f"{emoji} {job[0][:15]}...")

# Gradient Header
st.markdown("""
<div class="main-header">
    <h1>💼 Cover Letter Generator</h1>
    <p>AI-powered cover letters tailored to each job posting</p>
</div>
""", unsafe_allow_html=True)

# Step Progress Indicator
step = st.session_state.step
cols = st.columns(3)
steps = [("1️⃣", "Input"), ("2️⃣", "Generate"), ("3️⃣", "Download")]
for i, (icon, label) in enumerate(steps):
    with cols[i]:
        if i + 1 < step:
            st.markdown(f"<span class='step-complete'>{icon} {label} ✓</span>", unsafe_allow_html=True)
        elif i + 1 == step:
            st.markdown(f"<span class='step-active'>{icon} {label}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: #666;'>{icon} {label}</span>", unsafe_allow_html=True)

st.markdown("---")

if st.session_state.step == 1:
    st.header("📋 Step 1: Paste Job Posting")
    
    job_url = st.text_input("🔗 Job URL:")
    job_text = st.text_area("📝 Or paste job description:", height=200)
    
    if st.button("🔍 Analyze Job", type="primary"):
        input_content = job_url if job_url else job_text
        
        if input_content:
            with st.spinner("Analyzing..."):
                from scraper import process_job_input
                result = process_job_input(input_content, jina_key, cerebras_client)
                
                if result["success"]:
                    st.session_state.job_content = result["content"]
                    st.session_state.job_info["url"] = job_url
                    
                    # Get extracted info
                    extracted = result.get("job_info", {})
                    st.session_state.job_info["company"] = extracted.get("company", "")
                    st.session_state.job_info["title"] = extracted.get("title", "")
                    st.session_state.job_info["location"] = extracted.get("location", "")
                    
                    # Match skills
                    from skills import match_skills_keyword, match_transferable_skills
                    matched = match_skills_keyword(result["content"])
                    st.session_state.matched_skills = matched
                    
                    # Match transferable skills (Tableau→Power BI, Airflow→Dagster, etc.)
                    transferable = match_transferable_skills(result["content"])
                    st.session_state.transferable_skills = transferable
                    
                    # Match resumes to job
                    from resume_profiles import get_all_scores_sorted
                    cv_scores = get_all_scores_sorted(result["content"])
                    st.session_state.cv_scores = cv_scores
                    st.session_state.best_cv = cv_scores[0][0] if cv_scores else None
                    
                    # Company research - get mission, values, objectives (positives only)
                    company_name = st.session_state.job_info.get("company", "")
                    if company_name and tavily_key:
                        from search import search_company_mission
                        mission_result = search_company_mission(company_name, tavily_key)
                        if mission_result.get("success"):
                            st.session_state.company_research = mission_result.get("mission_values", "")
                        else:
                            st.session_state.company_research = ""
                    else:
                        st.session_state.company_research = ""
                    
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error')}")
        else:
            st.warning("Please enter a URL or paste text")

elif st.session_state.step == 2:
    st.header("✉️ Step 2: Generate Cover Letter")
    
    # Best CV Recommendation
    if st.session_state.get("best_cv"):
        best_cv = st.session_state.best_cv
        cv_scores = st.session_state.get("cv_scores", [])
        best_score = cv_scores[0][1] if cv_scores else {}
        st.success(f"🏆 **Best Resume Match: {best_score.get('profile_name', 'Unknown')}** ({best_score.get('score', 0)}% match)")
        if best_score.get("matched_skills"):
            st.caption(f"Matched: {', '.join(best_score['matched_skills'][:5])}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Job Details")
        company = st.text_input("Company:", st.session_state.job_info.get("company", ""))
        title = st.text_input("Job Title:", st.session_state.job_info.get("title", ""))
        location = st.text_input("Location:", st.session_state.job_info.get("location", ""))
        
        # Update session state
        st.session_state.job_info["company"] = company
        st.session_state.job_info["title"] = title
        st.session_state.job_info["location"] = location
    
    with col2:
        st.subheader("✅ Skills Matched")
        if st.session_state.matched_skills:
            for skill in st.session_state.matched_skills[:5]:
                st.markdown(f"✅ **{skill['skill'].title()}**")
        else:
            st.info("No exact matches, AI will generate based on job text")
        
        # Show transferable skills (Tableau→Power BI, etc.)
        if st.session_state.get("transferable_skills"):
            st.markdown("---")
            st.subheader("🔄 Transferable Skills")
            for t in st.session_state.transferable_skills[:3]:
                st.markdown(f"💡 Job wants **{t['job_needs'].title()}** → You have **{t['you_have'].title()}**")
        
        # Company research (auto-fetched from Tavily)
        if st.session_state.get("company_research"):
            st.markdown("---")
            st.subheader("🏢 Company Research")
            st.success("✅ Mission & values extracted (positives only)")
            with st.expander("View company research"):
                st.markdown(st.session_state.company_research)
    
    tone = st.selectbox("Tone:", ["confident", "formal", "conversational"], index=1)  # Default to formal
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🚀 Generate Cover Letter", type="primary"):
            if not cerebras_client:
                st.error("Cerebras API key required!")
            elif not company or not title:
                st.error("Please fill in Company and Job Title")
            else:
                with st.spinner("Generating..."):
                    from generator import generate_cover_letter, build_full_cover_letter
                    from skills import get_best_projects
                    
                    projects = get_best_projects(st.session_state.matched_skills)
                    transferable = st.session_state.get("transferable_skills", [])
                    company_research = st.session_state.get("company_research", "")
                    
                    opening = generate_cover_letter(
                        st.session_state.job_info,
                        st.session_state.matched_skills,
                        projects,
                        tone,
                        cerebras_client,
                        transferable  # Pass transferable skills
                    )
                    html = build_full_cover_letter(
                        opening,
                        st.session_state.job_info,
                        st.session_state.matched_skills,
                        projects,
                        company_research,
                        cerebras_client,
                        st.session_state.get("best_cv", "data_engineer")
                    )
                    st.session_state.cover_letter = html
                    st.session_state.step = 3
                    st.rerun()
    
    with col2:
        # Regenerate button if already generated
        if st.session_state.get("cover_letter"):
            if st.button("🔄 Regenerate (New Version)"):
                if not cerebras_client:
                    st.error("Cerebras API key required!")
                elif not company or not title:
                    st.error("Please fill in Company and Job Title")
                else:
                    with st.spinner("Regenerating..."):
                        from generator import generate_cover_letter, build_full_cover_letter
                        from skills import get_best_projects
                        
                        projects = get_best_projects(st.session_state.matched_skills)
                        transferable = st.session_state.get("transferable_skills", [])
                        company_research = st.session_state.get("company_research", "")
                        
                        opening = generate_cover_letter(
                            st.session_state.job_info,
                            st.session_state.matched_skills,
                            projects,
                            tone,
                            cerebras_client,
                            transferable
                        )
                        html = build_full_cover_letter(
                            opening,
                            st.session_state.job_info,
                            st.session_state.matched_skills,
                            projects,
                            company_research,
                            cerebras_client,
                            st.session_state.get("best_cv", "data_engineer")  # Resume type
                        )
                        st.session_state.cover_letter = html
                        st.session_state.step = 3
                        st.rerun()
    
    with col3:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()

elif st.session_state.step == 3:
    st.header("📄 Step 3: Your Cover Letter")
    
    # Preview with white background
    st.components.v1.html(st.session_state.cover_letter, height=600, scrolling=True)
    
    # Professionalism Review
    st.markdown("---")
    st.subheader("📊 Professionalism Review")
    
    from review import review_cover_letter, format_review_html
    review = review_cover_letter(st.session_state.cover_letter)
    
    # Score display
    st.markdown(format_review_html(review), unsafe_allow_html=True)
    
    # Checklist
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Passed:**")
        for item in review["passes"]:
            st.markdown(f"✅ {item['message']}")
    with col2:
        st.markdown("**⚠️ Suggestions:**")
        for item in review["errors"] + review["warnings"]:
            icon = "❌" if item["severity"] == "error" else "⚠️"
            st.markdown(f"{icon} {item['message']}")
    
    st.markdown("---")
    
    company = st.session_state.job_info.get("company", "Company")
    filename_base = f"CoverLetter_{company.replace(' ', '_')}"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📥 Download HTML",
            st.session_state.cover_letter,
            file_name=f"{filename_base}.html",
            mime="text/html"
        )
    
    with col2:
        # Show formatted plain text in text area for copying
        if st.button("📋 Show Plain Text"):
            st.session_state.show_plain_text = not st.session_state.get("show_plain_text", False)
    
    with col3:
        if st.button("🆕 New Job"):
            for key in defaults:
                st.session_state[key] = defaults[key]
            st.rerun()
    
    # Show plain text in expandable text area if requested
    if st.session_state.get("show_plain_text"):
        st.markdown("---")
        st.subheader("📋 Plain Text for Job Portals")
        st.caption("Copy this text and paste into job application portals")
        
        import re
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(st.session_state.cover_letter, 'html.parser')
        
        # Extract date
        date_elem = soup.find(class_='date')
        date_text = date_elem.get_text().strip() if date_elem else ""
        
        # Extract recipient
        recipient_elem = soup.find(class_='recipient')
        recipient_lines = recipient_elem.get_text().strip().split('\n') if recipient_elem else []
        
        # Extract subject
        subject_elem = soup.find(class_='subject')
        subject_text = subject_elem.get_text().strip() if subject_elem else ""
        
        # Extract body paragraphs
        body_paragraphs = []
        for p in soup.find_all(['p', 'div'], class_=['body-text', 'salutation']):
            text = p.get_text().strip()
            if text and text not in ['Cheers,']:
                body_paragraphs.append(text)
        
        # Extract projects list
        projects_list = soup.find(class_='projects')
        projects_text = ""
        if projects_list:
            projects_text = "\n\nKey Projects:\n"
            for li in projects_list.find_all('li'):
                projects_text += "• " + li.get_text().strip() + "\n"
        
        # Extract tech stack
        tech_elem = soup.find(class_='tech-stack')
        tech_text = ""
        if tech_elem:
            tech_text = "\n" + tech_elem.get_text().strip()
        
        # Build clean formatted text
        formatted_text = f"""{date_text}

{chr(10).join(recipient_lines)}

{subject_text}

{body_paragraphs[0] if body_paragraphs else ""}

{body_paragraphs[1] if len(body_paragraphs) > 1 else ""}{projects_text}{tech_text}

{chr(10).join(body_paragraphs[2:]) if len(body_paragraphs) > 2 else ""}

Cheers,
{PROFILE['name']}"""
        
        # Clean up excessive newlines
        formatted_text = re.sub(r'\n\n\n+', '\n\n', formatted_text)
        
        st.text_area(
            "Copy this text:",
            formatted_text,
            height=400,
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    st.subheader("💾 Save Application?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 I Applied!"):
            c = conn.cursor()
            c.execute("""
                INSERT INTO applications (company, title, location, url, status, created_at)
                VALUES (?, ?, ?, ?, 'Applied', ?)
            """, (
                st.session_state.job_info.get("company", ""),
                st.session_state.job_info.get("title", ""),
                st.session_state.job_info.get("location", ""),
                st.session_state.job_info.get("url", ""),
                datetime.now().isoformat()
            ))
            conn.commit()
            st.success("✅ Saved!")
            st.balloons()
    
    with col2:
        if st.button("📌 Save for Later"):
            c = conn.cursor()
            c.execute("""
                INSERT INTO applications (company, title, location, url, status, created_at)
                VALUES (?, ?, ?, ?, 'Saved', ?)
            """, (
                st.session_state.job_info.get("company", ""),
                st.session_state.job_info.get("title", ""),
                st.session_state.job_info.get("location", ""),
                st.session_state.job_info.get("url", ""),
                datetime.now().isoformat()
            ))
            conn.commit()
            st.success("✅ Saved for later!")

# Footer
st.markdown("---")
st.caption("Job Application Toolkit • Cerebras • Jina")
