# 📊 Financial Document Analyzer - Debug Challenge

An AI-powered pipeline that processes financial documents (PDFs) and produces:
- ✅ Financial summaries
- ✅ Investment recommendations
- ✅ Risk assessments

Built using [CrewAI](https://docs.crewai.com/), [FastAPI](https://fastapi.tiangolo.com/), and Google’s **Gemini** models.

Debugging Summary (Bugs Fixed)
1. requirements.txt
❌ Pydantic v1 with FastAPI ≥0.110 → crash
✅ Fixed by upgrading to pydantic==2.7.0

2. agents.py
❌ No API key validation
❌ Overly verbose prompts
✅ Added key check + simplified prompts

3. task.py
❌ {file_path} placeholder not resolved
❌ No clear stop if document invalid
✅ Added strict error message + simplified instructions

4. main.py
❌ Pipeline continued even if verification failed
❌ Weak file handling and query validation
✅ Stopped tasks on invalid docs + safe cleanup + default query

Setup and Usage Instructions

## 🚀 Getting Started

### 1. Clone the Repository
git clone https://github.com/<your-username>/financial-doc-analyzer.git
cd financial-doc-analyzer

2. Environment Setup
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3. Add API Key
GOOGLE_API_KEY=your_api_key_here

4. Run the Server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Health check → http://127.0.0.1:8000/
API docs → http://127.0.0.1:8000/docs # Upload and analysis of the Document here.

API Documentation

Endpoints
GET / → Health check
POST /analyze → Upload a financial document and run analysis

Inputs
file (PDF, required)
query (string, optional, default = comprehensive analysis request)

Outputs
Success → JSON with summary, recommendations, and risks
Failure → JSON with error message
