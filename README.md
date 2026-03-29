# ⚡ Agentic AI for Autonomous Enterprise Workflows
### ET AI Hackathon 2026 — Problem Statement 2

A multi-agent AI system that autonomously executes complex enterprise processes with self-correction, auditability, and minimal human involvement — powered by **Google Gemini**.

---

## 🏗️ Agent Architecture

```
User Request
     │
     ▼
┌─────────────────────┐
│  Orchestrator Agent │  ← Coordinates everything, handles retries & failures
└──────────┬──────────┘
           │
     ┌─────▼─────┐
     │  Phase 1  │
     │  Data     │  ← DataRetrievalAgent: fetches, validates enterprise data
     │  Retrieval│
     └─────┬─────┘
           │
     ┌─────▼─────┐
     │  Phase 2  │
     │  Decision │  ← DecisionAgent: applies business rules, routes approvals
     └─────┬─────┘
           │
     ┌─────▼─────┐
     │  Phase 3  │
     │  Action   │  ← ActionAgent: executes approved steps autonomously
     │  Execution│
     └─────┬─────┘
           │
     ┌─────▼─────┐
     │  Phase 4  │
     │ Verifica- │  ← VerificationAgent: independently validates outcomes
     │   tion    │
     └─────┬─────┘
           │
     Audit Trail + Result
```

---

## 📁 Directory Structure

```
enterprise_workflow_agent/
├── agents/
│   ├── orchestrator.py          # Master coordinator with retry logic
│   ├── data_retrieval_agent.py  # Data fetching & validation
│   ├── decision_agent.py        # Business rules & approval routing
│   ├── action_agent.py          # Step execution
│   └── verification_agent.py   # Independent quality verification
├── tools/
│   └── workflow_tools.py        # Simulated enterprise system integrations
├── ui/
│   └── dashboard.py             # Streamlit web dashboard
├── utils/
│   ├── audit_logger.py          # Immutable audit trail
│   └── state_manager.py         # Workflow state persistence
├── data/
│   ├── audit/                   # Per-workflow audit JSON files
│   └── logs/                    # Workflow state files
├── config.py                    # Gemini API + workflow definitions
├── main.py                      # CLI entry point
├── requirements.txt
└── .env                         # Your API key goes here
```

---

## 🚀 Setup & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Set your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your key at: https://aistudio.google.com/app/apikey

### Step 3a — Run the Web Dashboard (recommended)
```bash
streamlit run ui/dashboard.py
```
Then open http://localhost:8501 in your browser.

### Step 3b — Run CLI Demo
```bash
python main.py
```

---

## 🔄 Supported Workflows

| Workflow | Steps | SLA |
|----------|-------|-----|
| Employee Onboarding | 8 steps | 48 hrs |
| Procurement to Payment | 9 steps | 72 hrs |
| Contract Lifecycle | 8 steps | 120 hrs |
| Meeting Intelligence | 8 steps | 24 hrs |

---

## 🛠️ Tech Stack
- **LLM**: Google Gemini 2.5 Flash
- **Orchestration**: Custom multi-agent pipeline (Python)
- **UI**: Streamlit
- **State**: JSON persistence with full audit trail
