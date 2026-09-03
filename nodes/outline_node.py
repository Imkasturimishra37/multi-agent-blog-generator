from agents.outline_agent import generate_outline
from state.blog_state import BlogState


def outline_node(state: BlogState):

    research_data = {
        "topic": state["topic"],
        "research_summary": state["research_summary"],
    }

    outline = generate_outline(
        research_data,
        state.get("feedback", "")
    )

    return {
        "outline": outline
    }
