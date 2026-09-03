from agents.research_agent import research_topic
from state.blog_state import BlogState


def research_node(state: BlogState):

    research = research_topic(
        topic=state["topic"],
        pdf_context=state.get("retrieved_context", "")
    )

    return {
        "research_summary": research["research_summary"],
        "search_results": research["search_results"],
        "pdf_context": research["pdf_context"]
    }