from agents.writer_agent import generate_blog
from state.blog_state import BlogState


def writer_node(state: BlogState):

    research_data = {
        "topic": state["topic"],
        "research_summary": state["research_summary"],
    }

    blog = generate_blog(
        research_data,
        state["outline"]
    )

    return {
        "blog": blog
    }