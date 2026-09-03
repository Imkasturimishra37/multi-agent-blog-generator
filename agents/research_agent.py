from langchain_community.tools import DuckDuckGoSearchResults
from config import llm

search = DuckDuckGoSearchResults()


def research_topic(topic: str, pdf_context: str = ""):
    """
    Research a topic using DuckDuckGo.
    If PDF context is provided, combine it with web search.
    """

    # Search the web
    search_results = search.invoke(topic)

    # If no PDF uploaded
    if pdf_context.strip() == "":
        context = f"""
        Web Search Results:

        {search_results}
        """

    # If PDF uploaded
    else:
        context = f"""
        Web Search Results:

        {search_results}


        PDF Context:

        {pdf_context}
        """

    prompt = f"""
    You are a professional research assistant.

    Topic:
    {topic}

    Use the information below to prepare a research summary.

    {context}

    Instructions:

    - Combine information intelligently.
    - Give priority to PDF information if it conflicts with web search.
    - Remove duplicate information.
    - Return only important bullet points.
    - Keep the summary concise.
    """

    response = llm.invoke(prompt)

    return {
        "topic": topic,
        "research_summary": response.content,
        "search_results": search_results,
        "pdf_context": pdf_context
    }
