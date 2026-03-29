import streamlit as st
import json
import sys
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agents.orchestrator import OrchestratorAgent
from config import WORKFLOW_TYPES
from utils.state_manager import WorkflowState

st.set_page_config(
    page_title="NEURAL-OPS | Enterprise AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }

    .stButton>button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: 700;
        text-transform: uppercase;
        width: 100%;
    }

    .agent-log {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00f2fe;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px;
        border-left: 3px solid #00f2fe;
        margin: 5px 0;
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 30, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color: #00f2fe;'>NEURAL-OPS</h1>", unsafe_allow_html=True)
    st.markdown("`v3.0.4 - AGENTIC KERNEL` (PS2)")
    st.divider()

    page = st.radio("SYSTEM NAVIGATION", ["🚀 EXECUTE WORKFLOW", "📊 NETWORK HEALTH", "🔍 AUDIT CORE"],
                    label_visibility="collapsed")

    st.divider()
    st.markdown("### 🧬 ACTIVE SWARM")
    for icon, name in [("🎯", "Orchestrator"), ("🔍", "Retriever"), ("🧠", "Cognitive"), ("⚙️", "Executor"),
                       ("✅", "Validator")]:
        st.markdown(f"{icon} **{name}**")

if "🚀" in page:
    st.markdown('<h1 class="main-header">AUTONOMOUS KERNEL</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 1.2rem; color: #888;'>Orchestrating complex enterprise processes with built-in self-correction.</p>",
        unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📡 WORKFLOW CONFIG")
        workflow_type = st.selectbox(
            "Select Deployment Protocol",
            options=list(WORKFLOW_TYPES.keys()),
            format_func=lambda x: WORKFLOW_TYPES[x]["name"]
        )
        wf = WORKFLOW_TYPES[workflow_type]
        st.markdown(f"**Description:** {wf['description']}")
        st.markdown(f"**SLA Priority:** `{wf['sla_hours']} Hours`")

        steps_html = "".join([f"<span style='color:#00f2fe;'>{s.upper()}</span> → " for s in wf["steps"][:3]]) + "..."
        st.markdown(f"**Chain:** {steps_html}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💾 PARAMETERS")

        input_data = {}
        if workflow_type == "employee_onboarding":
            input_data = {
                "name": st.text_input("FULL NAME", "Rahul Sharma"),
                "employee_id": st.text_input("ID TAG", "EMP-2026-X"),
                "department": st.selectbox("UNIT", ["Engineering", "HR", "Operations"])
            }
        elif workflow_type == "procurement_to_payment":
            input_data = {
                "item": st.text_input("ASSET NAME", "Nvidia H100 GPU"),
                "quantity": st.number_input("QTY", min_value=1, value=1),
                "amount": st.number_input("VALUATION (₹)", min_value=0.0, value=250000.0)
            }
        elif workflow_type == "contract_lifecycle":
            input_data = {
                "parties": st.text_input("LEGAL ENTITIES", "Google, OpenAI"),
                "contract_type": st.selectbox("LEGAL FRAMEWORK", ["NDA", "SLA", "MOU"]),
                "value": st.number_input("CONTRACT VALUE (₹)", min_value=0.0, value=10000000.0)
            }
        else:
            input_data = {"req_id": "DEFAULT_SYS_GEN"}
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⚡ INITIALIZE AUTONOMOUS EXECUTION"):
        st.divider()
        st.markdown("### ⚡ LIVE SWARM COORDINATION")

        progress_box = st.empty()
        progress_entries = []


        def update_ui(step, message, agent):
            progress_entries.append(f"<div class='agent-log'>[{agent.upper()}] {message}</div>")
            with progress_box.container():
                st.markdown("".join(progress_entries[-6:]), unsafe_allow_html=True)


        with st.spinner("SYSTÈME EN COURS..."):
            try:
                orchestrator = OrchestratorAgent()
                result = orchestrator.run_workflow(workflow_type, input_data, progress_callback=update_ui)
            except Exception as e:
                st.error(f"FATAL KERNEL ERROR: {e}")
                st.stop()

        st.balloons()
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:#00f2fe;'>WORKFLOW {result.get('workflow_id')} : {result.get('status')}</h2>",
                    unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AUDIT HITS", result.get("audit_summary", {}).get("total_actions", 0), delta="LIVE")
        m2.metric("COGNITIVE SCORE", f"{result.get('verification', {}).get('quality_score', 0)}%", delta="OPTIMIZED")
        m3.metric("RISK FACTOR", result.get("decision", {}).get("risk_level", "LOW"))
        m4.metric("SLA COMPLIANCE", "PASSED" if result.get("verification", {}).get("sla_met") else "RISK")
        st.markdown('</div>', unsafe_allow_html=True)

elif "📊" in page:
    st.markdown('<h1 class="main-header">NETWORK ANALYTICS</h1>', unsafe_allow_html=True)
    states = WorkflowState.list_all()
    if states:
        st.dataframe(states, use_container_width=True)
    else:
        st.info("NO ACTIVE SIGNALS DETECTED.")

elif "🔍" in page:
    st.markdown('<h1 class="main-header">AUDIT DATABASE</h1>', unsafe_allow_html=True)
    states = WorkflowState.list_all()
    if states:
        choice = st.selectbox("Select Trace ID", [s["workflow_id"] for s in states])
        st.code(f"LOADING TRACE: {choice}...", language='bash')

        audit_file_path = os.path.join(ROOT, "data", "audit", f"{choice}.json")

        if os.path.exists(audit_file_path):
            with open(audit_file_path, 'r') as f:
                audit_data = json.load(f)

            st.markdown(f"### 📑 TRACE LOGS: `{choice}`")
            for entry in audit_data:
                st.markdown(f"**{entry.get('agent')}** executed `{entry.get('action')}`")
                st.caption(f"Status: {entry.get('status')} | {entry.get('timestamp')}")
                st.json(entry.get("details", {}))
                st.divider()
        else:
            st.error(f"AUDIT LOG NOT FOUND: `{audit_file_path}`")
    else:
        st.info("NO AUDIT RECORDS IN STORAGE.")