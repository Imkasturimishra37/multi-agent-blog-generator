from typing import TypedDict

class BlogState(TypedDict):

    topic: str

    pdf_context: str          # Optional PDF text
    retrieved_context: str    # Context returned by RAG

    research_summary: str
    search_results: str

    outline: str

    approved: bool
    feedback: str

    blog: str
    reviewed_blog: str
    fact_checked_blog: str
    final_blog: str
