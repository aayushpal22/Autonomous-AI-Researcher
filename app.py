import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from persistence import save_research_report
import time

# Load environment
load_dotenv()

# Initialize ai
@st.cache_resource
def init_ai():
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
    Query: {query}
    
    Search Results: {search_results}
    
    Create simple research report:
    1. **Summary** (5 bullets)
    2. **Key Points** 
    3. **Sources**
    """)
    chain = (
        {"search_results": search_tool, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def main():
    st.set_page_config(page_title="AI Researcher", layout="wide")
    
    st.title("🤖 Autonomous AI Researcher")
    st.markdown("**Ask ANY question → Get instant research report!**")
    
    
    with st.sidebar:
        st.header("🔍 Settings")
        st.info("✅ Live web search + AI analysis")
        st.info("💾 Reports auto-saved")
        st.success("🆓 FREE: Groq + Tavily APIs")
    
   
    query = st.text_input(
        "Enter your question:",
        placeholder="How does AI help farmers?",
        label_visibility="collapsed"
    )
    
    if st.button("🔎 Research Now", type="primary"):
        if query:
            with st.spinner("🔎 Searching web... 📝 AI analyzing..."):
                try:
                    chain = init_ai()
                    report = chain.invoke(query)
                    
                    
                    filepath = save_research_report(query, report)
                    
                    
                    st.success("✅ Research Complete!")
                    st.markdown("### 📄 Research Report")
                    st.markdown(report)
                    
                    st.info(f"💾 **Saved:** `{filepath}`")
                    
                    
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"research_{int(time.time())}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.info("💡 Check API keys in `.env`")
        else:
            st.warning("❌ Enter a question first!")
    
  
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌾 AI for farmers"):
            st.text_input("", "How does AI help farmers grow more crops?", key="q1")
    with col2:
        if st.button("🚜 Plant diseases"):
            st.text_input("", "How AI finds sick plants", key="q2")
    with col3:
        if st.button("💧 Smart water"):
            st.text_input("", "How AI saves water in farming", key="q3")
    with col4:
        if st.button("📱 Phone apps"):
            st.text_input("", "AI plant apps for phone", key="q4")

if __name__ == "__main__":
    main()
