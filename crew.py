from crewai import Task, Crew, Process
from agents import (
    create_researcher_agent, 
    create_summarizer_agent, 
    create_synthesizer_agent
)

def create_research_crew(query: str):
    researcher = create_researcher_agent()
    summarizer = create_summarizer_agent()
    synthesizer = create_synthesizer_agent()
    
    research_task = Task(
        description=f"Research the technology topic: '{query}'. Use web search to find 8-12 high-quality sources.",
        expected_output="Markdown list of 8-12 sources with URLs and descriptions.",
        agent=researcher
    )
    
    summarize_task = Task(
        description="Review web research results. Extract key insights from top 5-7 sources.",
        expected_output="Structured summary with Key Trends, Technical Details.",
        context=[research_task],
        agent=summarizer
    )
    
    synthesis_task = Task(
        description="Write complete technology research report with Executive Summary and Key Findings.",
        expected_output="Complete markdown research report.",
        context=[research_task, summarize_task],
        agent=synthesizer
    )
    
    
    crew = Crew(
        agents=[researcher, summarizer, synthesizer],
        tasks=[research_task, summarize_task, synthesis_task],
        process=Process.sequential,
        verbose=True,
        memory=False,          
        embedder=None,       
        knowledge=None,        
        database=False,        
        function_calling_llm=None  
    )
    
    return crew
