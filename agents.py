from crewai import Agent
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL
from tools import get_tools

llm = ChatGroq(
    model=LLM_MODEL,
    temperature=0.1,
    api_key=GROQ_API_KEY
)

def create_researcher_agent():
    return Agent(
        role="Technology Web Researcher",
        goal=(
            "Find the most relevant, recent, high-quality sources about technology "
            "topics (AI, chips, cloud, software, hardware, etc.). Prioritize "
            "engineering blogs, docs, research papers, and official announcements."
        ),
        backstory=(
            "You are a senior technology analyst with 15+ years experience. "
            "You excel at finding credible sources and understanding complex "
            "technical topics quickly."
        ),
        llm=llm,
        tools=get_tools(),
        verbose=True,
        max_iter=5,
        allow_delegation=False,  
        memory=False,
        embedder=None,
        knowledge=None,
        database=False
    )

def create_summarizer_agent():
    return Agent(
        role="Technical Content Summarizer",
        goal=(
            "Read web search results and URLs, then extract key insights, "
            "architectures, numbers, tradeoffs, and trends from technology content."
        ),
        backstory=(
            "You are a technical writer who distills complex technical documents "
            "into clear, structured summaries for CTOs and engineers."
        ),
        llm=llm,
        verbose=True,
        max_iter=4,
        allow_delegation=False,  
        memory=False,
        embedder=None,
        knowledge=None,
        database=False
    )

def create_synthesizer_agent():
    return Agent(
        role="Technology Research Lead",
        goal=(
            "Synthesize all research findings into a comprehensive technology "
            "research brief with executive summary, key findings, and citations."
        ),
        backstory=(
            "You write research reports for enterprise CTOs. Your reports are "
            "clear, structured, and actionable with inline citations."
        ),
        llm=llm,
        verbose=True,
        max_iter=4,
        allow_delegation=False,  
        memory=False,
        embedder=None,
        knowledge=None,
        database=False
    )
