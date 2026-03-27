from crewai_tools import TavilySearchTool
from config import TAVILY_API_KEY

def get_tools():
    """Returns configured tools for the research crew."""
    return [
        TavilySearchTool(
            api_key=TAVILY_API_KEY,
            max_results=10,
            search_depth="advanced"
        )
    ]
