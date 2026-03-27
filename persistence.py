import os
from datetime import datetime
import re  

KNOWLEDGE_BASE_DIR = "./knowledge_base"

os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

def slugify(text):
    """Python 3 compatible slugify (no unicode errors)"""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)  
    text = re.sub(r'\s+', '-', text)          
    return text.strip('-')

def save_research_report(query: str, report: str) -> str:
    """Save research report to knowledge base."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    query_slug = slugify(query)[:80] or "research"
    filename = f"{timestamp}_{query_slug}.md"
    filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
    
    metadata = f"""# Technology Research Report
**Query**: {query}
**Generated**: {datetime.now().isoformat()}

---
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(metadata + str(report))
    
    return filepath
