# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from utils.rag import build_embeddings, query_vector_store
from utils.skills_analyzer import extract_skills, generate_ats_suggestions
from utils.job_scraper import search_jobs_comprehensive, match_jobs_to_skills
from utils.application_helper import generate_cover_letter, generate_interview_prep
from models.llm import get_chat_model
from utils.text_modes import format_response
from pypdf import PdfReader
from langchain_core.messages import SystemMessage, HumanMessage

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="CareerTrackAI", layout="wide", initial_sidebar_state="expanded")
load_dotenv()

# ---------------- SESSION STATE ---------------- #
if "messages" not in st.session_state: st.session_state.messages = []
if "skills_data" not in st.session_state: st.session_state.skills_data = None
if "resume_content" not in st.session_state: st.session_state.resume_content = None
if "response_mode" not in st.session_state: st.session_state.response_mode = "Detailed"
if "job_location" not in st.session_state: st.session_state.job_location = "Remote"

# ---------------- STYLES ---------------- #
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.main .block-container {padding: 0 !important; max-width: 100% !important;}
section[data-testid="stSidebar"] {width: 280px !important; background-color: #171717 !important;}
section[data-testid="stSidebar"] > div {padding: 1rem !important;}
section[data-testid="stSidebar"] label {color: #9ca3af !important; font-size: 0.85rem !important; font-weight: 500 !important;}

.compact-header {position: fixed; top: 0; left: 280px; right: 0; z-index: 999; background-color: #0e1117; padding: 0.875rem 2rem; border-bottom: 1px solid #2d2d2d;}
.compact-header h1 {margin: 0; font-size: 1rem; font-weight: 600; color: #e5e7eb;}
.main-content {margin-top: 56px; margin-left: 280px; padding: 1.5rem 2rem 140px 2rem; min-height: calc(100vh - 200px);}

.bottom-fixed {position: fixed; bottom: 0; left: 280px; right: 0; background: linear-gradient(180deg, transparent, #0e1117 15%); padding: 1rem 2rem 1.5rem 2rem; z-index: 998;}
.tool-buttons {display: flex; gap: 0.5rem; margin-bottom: 0.75rem; justify-content: center;}

.stButton > button {
    background-color: #1f2937 !important; color: #d1d5db !important; border: 1px solid #374151 !important;
    border-radius: 20px !important; padding: 0.6rem 1.5rem !important; font-size: 0.875rem !important;
    font-weight: 500 !important; height: auto !important; min-height: 40px !important;
    transition: all 0.2s !important; white-space: nowrap !important; overflow: visible !important;
}
.stButton > button:hover {background-color: #374151 !important; border-color: #4b5563 !important; transform: translateY(-1px);}

.stChatInput > div {background-color: #1f2937 !important; border: 1px solid #374151 !important; border-radius: 24px !important;}
.stChatInput input {color: #e5e7eb !important; font-size: 0.95rem !important;}
.stChatMessage {padding: 1.5rem 2rem !important; background-color: transparent !important; border-radius: 0 !important;}
.stChatMessage[data-testid="assistant-message"] {background-color: #1a1a1a !important;}

.processing-box {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white; padding: 0.875rem 1.25rem; border-radius: 8px; text-align: center;
    font-weight: 500; font-size: 0.95rem; animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {0%, 100% {opacity: 1;} 50% {opacity: 0.75;}}

.stSelectbox, .stMultiSelect {margin-bottom: 1rem !important;}
.stRadio {margin-top: 1rem !important;}
.stRadio > div {flex-direction: row !important; gap: 1rem !important;}
section[data-testid="stFileUploader"] {background-color: #1f2937; padding: 1rem; border-radius: 8px; border: 1px solid #374151;}
.resume-card {background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 1rem; border-radius: 8px; border-left: 3px solid #3b82f6; margin-top: 1rem;}

@media (max-width: 768px) {.compact-header, .bottom-fixed, .main-content {left: 0; margin-left: 0;}}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    uploaded_files = st.file_uploader("Upload resume(s) - TXT or PDF", type=["txt","pdf"], accept_multiple_files=False, key="resume_upload")
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af; font-size:0.75rem; margin-bottom:0.75rem; font-weight:600; letter-spacing:0.5px;'>⚙️ SETTINGS</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9ca3af; font-size:0.8rem; margin-bottom:0.25rem;'>Location</p>", unsafe_allow_html=True)
    locations = ["Remote", "United States", "India", "United Kingdom", "Canada", "Germany", "Singapore", "Australia"]
    st.session_state.job_location = st.selectbox("loc", locations, index=0, label_visibility="collapsed")
    
    st.markdown("<p style='color:#9ca3af; font-size:0.8rem; margin-bottom:0.25rem;'>Experience</p>", unsafe_allow_html=True)
    experience_level = st.selectbox("exp", ["All Levels", "Entry Level", "Mid Level", "Senior", "Lead"], label_visibility="collapsed")
    
    st.markdown("<p style='color:#9ca3af; font-size:0.8rem; margin-bottom:0.25rem;'>Job type</p>", unsafe_allow_html=True)
    job_type = st.multiselect("type", ["Full-time", "Part-time", "Contract", "Internship"], default=["Full-time"], label_visibility="collapsed")
    
    st.markdown("<p style='color:#9ca3af; font-size:0.8rem; margin-bottom:0.25rem; margin-top:1rem;'>Response Style</p>", unsafe_allow_html=True)
    st.session_state.response_mode = st.radio("mode", ["Detailed", "Concise"], horizontal=True, label_visibility="collapsed")
    
    if st.session_state.resume_content and st.session_state.skills_data:
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #374151;'/>", unsafe_allow_html=True)
        skills_data = st.session_state.skills_data
        tech_skills = ', '.join(skills_data.get('technical_skills',[])[:6])
        industries = ', '.join(skills_data.get('detected_industries',[]))
        experience = skills_data.get('total_experience',0)
        st.markdown(f"""
        <div class="resume-card">
            <p style='color:#60a5fa; font-size:0.75rem; font-weight:600; margin:0 0 0.75rem 0;'>📊 RESUME SUMMARY</p>
            <div style='font-size:0.75rem; line-height:1.6; color:#d1d5db;'>
                <div style='margin-bottom:0.5rem;'><strong style='color:#9ca3af;'>Skills:</strong> {tech_skills}</div>
                <div style='margin-bottom:0.5rem;'><strong style='color:#9ca3af;'>Industry:</strong> {industries}</div>
                <div><strong style='color:#9ca3af;'>Experience:</strong> {experience} years</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- Resume Processing ---------------- #
if uploaded_files:  # single file upload
    os.makedirs("knowledge_base", exist_ok=True)
    
    # Clear old knowledge base files
    for f in os.listdir("knowledge_base"):
        os.remove(os.path.join("knowledge_base", f))

    # Save uploaded resume
    path = os.path.join("knowledge_base", uploaded_files.name)
    with open(path, "wb") as fh:
        fh.write(uploaded_files.read())

    # Extract text
    text = ""
    if uploaded_files.name.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    elif uploaded_files.name.lower().endswith(".pdf"):
        pdf = PdfReader(path)
        text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

    # Save to session
    st.session_state.resume_content = text

    # Extract skills and build embeddings
    try: 
        st.session_state.skills_data = extract_skills(text)
        build_embeddings()
    except:
        st.session_state.skills_data = None

# ---------------- HEADER ---------------- #
st.markdown('<div class="compact-header"><h1>CareerTrackAI</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ---------------- Initialize LLM ---------------- #
try: chat_model = get_chat_model()
except: st.error("❌ Add API key to .env file"); st.stop()

# ---------------- Display Chat History ---------------- #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BOTTOM SECTION ---------------- #
st.markdown('<div class="bottom-fixed">', unsafe_allow_html=True)

def process_query(prompt):
    if not st.session_state.resume_content:
        st.warning("⚠️ Upload resume first")
        return
    
    # Process directly
    rag_context = ""
    try: 
        rag_chunks = query_vector_store(prompt, top_k=5)
        rag_context = "\n\n".join(rag_chunks) if rag_chunks else ""
    except: pass

    skills_analysis = st.session_state.skills_data
    job_results = None
    if any(k in prompt.lower() for k in ["job","find","position","opening"]):
        try:
            top_skills = skills_analysis.get('technical_skills', [])[:5] if skills_analysis else []
            industries = skills_analysis.get('detected_industries', []) if skills_analysis else []
            search_q = f"{industries[0]} {' '.join(top_skills[:3])}" if industries else ' '.join(top_skills) or prompt
            jobs = search_jobs_comprehensive(query=search_q, location=st.session_state.job_location, experience_level=experience_level, job_type=job_type, num_results=20)
            if jobs and skills_analysis: job_results = match_jobs_to_skills(jobs, skills_analysis)
            else: job_results = jobs
        except: pass

    application_help = None
    if any(k in prompt.lower() for k in ['cover letter','application','interview','ats','resume','cv']):
        resume_text = st.session_state.get('resume_content', rag_context)
        try:
            if 'cover letter' in prompt.lower(): application_help = {'type':'cover_letter','content':generate_cover_letter(resume_text,prompt)}
            elif 'interview' in prompt.lower(): application_help = {'type':'interview','content':generate_interview_prep(resume_text,prompt)}
            elif 'ats' in prompt.lower() or 'resume' in prompt.lower(): application_help = {'type':'ats','content':generate_ats_suggestions(resume_text)}
        except: pass

    context_parts = []
    if rag_context: context_parts.append(f"=== RESUME ===\n{rag_context[:2000]}")
    if skills_analysis: context_parts.append(f"=== SKILLS ===\nTechnical: {', '.join(skills_analysis.get('technical_skills',[])[:20])}\nIndustries: {', '.join(skills_analysis.get('detected_industries',[]))}\nExperience: {skills_analysis.get('total_experience',0)} years")
    if job_results:
        jobs_summary = []
        for job in job_results[:8]:
            jobs_summary.append(f"• **{job.get('title')}** at {job.get('company')} ({job.get('location')}) - {job.get('match_score', 'N/A')}% match - [Apply]({job.get('url', '#')})")
        context_parts.append("=== JOBS ===\n" + "\n".join(jobs_summary))
    if application_help: context_parts.append(f"=== HELP ===\n{application_help['content'][:1000]}")
    full_context = "\n\n".join(context_parts) or "No context."

    # Customize system message based on query type
    if job_results:
        system_message = f"You are a professional career advisor.\n\nContext:\n{full_context}\n\nMode: {st.session_state.response_mode}\n\nIMPORTANT: When showing job listings, include the provided [Apply](url) links exactly as given."
    else:
        system_message = f"You are a professional career advisor.\n\nContext:\n{full_context}\n\nMode: {st.session_state.response_mode}\n\nIMPORTANT: Do not include any placeholder links or 'Apply' buttons. Provide direct, actionable advice."

    try:
        messages = [SystemMessage(content=system_message), HumanMessage(content=prompt)]
        detailed_response = chat_model.invoke(messages).content
        if st.session_state.response_mode == "Concise":
            response_text = format_response(detailed_response, "Concise", chat_model)
        else:
            response_text = detailed_response
    except Exception as e: 
        response_text = f"❌ Error: {e}"

    # Add both messages at once
    st.session_state.messages.append({"role":"user","content":prompt})
    st.session_state.messages.append({"role":"assistant","content":response_text})
    st.rerun()

st.markdown('<div class="tool-buttons">', unsafe_allow_html=True)
cols = st.columns([1,1,1,1,1])
with cols[0]:
    if st.button("📝 Analyze", key="t1", use_container_width=True): 
        process_query("ATS score: Analyze my resume for ATS score and improvements.")
with cols[1]:
    if st.button("📊 Skills", key="t2", use_container_width=True): process_query("Show my skill gaps and learning suggestions.")
with cols[2]:
    if st.button("💼 Jobs", key="t3", use_container_width=True): process_query(f"Find {st.session_state.job_location} jobs matching my skills.")
with cols[3]:
    if st.button("✉️ Cover Letter", key="t4", use_container_width=True): process_query("Generate a professional cover letter.")
with cols[4]:
    if st.button("🎯 Career", key="t5", use_container_width=True): process_query("Suggest optimal career paths.")
st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Message CareerTrackAI...")
if user_input:
    process_query(user_input)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<script>setTimeout(() => window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"}), 100);</script>', unsafe_allow_html=True)