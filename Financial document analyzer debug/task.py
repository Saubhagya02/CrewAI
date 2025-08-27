from crewai import Task
from tools import file_read_tool
from agents import verifier, financial_analyst, investment_advisor, risk_assessor

# ------------------ TASKS ------------------

# Task to verify the document
verification_task = Task(
    description=(
        "Step 1: Verify the document.\n"
        "Read the file at the path provided in context.\n"
        "Decide if it is a financial report (annual/quarterly/earnings/financial statement).\n"
        "If it is NOT a financial report, return exactly:\n"
        "'Error: The provided document is not a financial report.'"
    ),
    expected_output=(
        "Either a confirmation with extracted text if valid, "
        "or 'Error: The provided document is not a financial report.'"
    ),
    agent=verifier,
    tools=[file_read_tool]
)

# Task for the financial analyst
financial_summary_task = Task(
    description=(
        "Step 2: Summarize the financial document.\n"
        "Extract key highlights: revenue, net income, margins, and trends.\n"
        "Provide a factual summary only (no advice or risks)."
    ),
    expected_output=(
        "A structured financial summary with bullet points of key metrics and performance trends."
    ),
    agent=financial_analyst,
    context=[verification_task]
)

# Task for the investment advisor
investment_analysis_task = Task(
    description=(
        "Step 3: Give investment recommendations.\n"
        "Use the summary to provide advice for 3 risk profiles:\n"
        "- Conservative\n"
        "- Moderate\n"
        "- Aggressive\n"
        "Each recommendation must cite data from the summary."
    ),
    expected_output=(
        "Recommendations grouped by risk profile, each supported with reasoning and financial data."
    ),
    agent=investment_advisor,
    context=[financial_summary_task]
)

# Task for the risk assessor
risk_assessment_task = Task(
    description=(
        "Step 4: Identify risks.\n"
        "Categorize risks into Market, Financial, and Operational.\n"
        "Explain potential impact of each."
    ),
    expected_output=(
        "A structured risk report with sections: Market Risks, Financial Risks, Operational Risks."
    ),
    agent=risk_assessor,
    context=[financial_summary_task]
)
# Note: Each task can access the 'file_path' from the initial context if needed.