## Importing libraries and files
import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import file_read_tool

# Load environment variables from .env file
load_dotenv()

# Ensure API key exists
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError(
        "❌ GOOGLE_API_KEY is missing. Please add it to your .env file."
    )

### Loading LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2,
)

# ------------------ AGENTS ------------------

# Document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Check if the uploaded file is a financial report. Stop analysis if it’s not.",
    verbose=True,
    memory=True,
    backstory=(
        "You ensure only financial reports (quarterly/annual reports, financial statements)"
        " are analyzed. Halt the process if the document is invalid."
    ),
    tools=[file_read_tool],
    llm=llm,
    allow_delegation=False
)

# Financial analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide a structured summary of the financial document with key metrics and trends.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in corporate finance with 20+ years of experience."
        " You extract objective insights from financial statements."
    ),
    tools=[file_read_tool],
    llm=llm,
    allow_delegation=False
)

# Investment advisor agent
investment_advisor = Agent(
    role="Prudent Investment Advisor",
    goal="Give investment recommendations for conservative, moderate, and aggressive investors.",
    verbose=True,
    memory=True,
    backstory=(
        "You provide clear, risk-adjusted investment strategies."
        " Your advice is directly linked to the company’s financial health."
    ),
    tools=[file_read_tool],
    llm=llm,
    allow_delegation=False
)

# Risk assessor agent
risk_assessor = Agent(
    role="Corporate Risk Assessor",
    goal="Identify market, operational, and financial risks from the report with mitigation ideas.",
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in risk management and build structured profiles of"
        " potential pitfalls in corporate performance."
    ),
    tools=[file_read_tool],
    llm=llm,
    allow_delegation=False
)
