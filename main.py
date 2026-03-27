import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate  # ✅ MODERN IMPORT
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from persistence import save_research_report
from datetime import datetime

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)


search_tool = TavilySearchResults(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=10
)


prompt = PromptTemplate.from_template("""
You are a technology research expert. Analyze these web search results for: {query}

Search Results:
{search_results}

Create a professional markdown report:
1. **Executive Summary** (5-8 bullets)
2. **Key Findings** (3-5 sections)  
3. **Technical Details** (numbers, benchmarks)
4. **Sources** (URLs)

Focus on actionable CTO insights. Use [Source 1] citations.
""")


chain = (
    {"search_results": search_tool, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def main():
    print("🤖 Autonomous Technology Researcher (Groq + Tavily)")
    print("=" * 60)
    
    while True:
        query = input("\n🔍 Enter technology research query (or 'quit'):\n> ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not query:
            print("❌ Enter a valid query.")
            continue
        
        print(f"\n🚀 Researching: '{query}'")
        print("⏳ Live web search + AI analysis...\n")
        
        try:
           
            print("🔎 Searching web...")
            print("📝 AI analyzing...")
            report = chain.invoke(query)
            
          
            filepath = save_research_report(query, report)
            
           
            print("✅ COMPLETE!")
            print(f"📄 Saved: {filepath}")
            print("\n📋 Preview:")
            print("-" * 80)
            preview = report[:2000] + "..." if len(report) > 2000 else report
            print(preview)
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\n⏹️  Cancelled.")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Check GROQ_API_KEY + TAVILY_API_KEY in .env")

if __name__ == "__main__":
    main()
