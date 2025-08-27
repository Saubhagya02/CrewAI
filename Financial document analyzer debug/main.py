from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from task import verification_task, financial_summary_task, investment_analysis_task, risk_assessment_task

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    """Run the analysis pipeline with the given query and file path."""
    
    tasks = [
        verification_task,
        financial_summary_task,
        investment_analysis_task,
        risk_assessment_task
    ]

    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Run pipeline
    result = financial_crew.kickoff({"query": query, "file_path": file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "✅ Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive analysis of this financial document, including a summary, investment recommendations, and a risk assessment.")
):
    """Upload and analyze a financial document (PDF)."""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        query = query.strip()
        if not query:
            query = "Provide a comprehensive analysis of this financial document, including a summary, investment recommendations, and a risk assessment."
            
        # Run crew pipeline
        response = run_crew(query=query, file_path=file_path)

        # Check if verification failed
        if isinstance(response, str) and "not a financial report" in response.lower():
            return {
                "status": "failed",
                "message": response,
                "file_processed": file.filename
            }
        
        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
