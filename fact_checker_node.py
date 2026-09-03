from agents.fact_checker import fact_check_blog
from state.blog_state import BlogState


def fact_checker_node(state: BlogState):

    research_data = {
        "research_summary": state["research_summary"]
    }

    checked = fact_check_blog(
        research_data,
        state["reviewed_blog"]
    )

    return {
        "fact_checked_blog": checked
    }