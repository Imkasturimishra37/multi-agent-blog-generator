from agents.seo_agent import optimize_seo
from state.blog_state import BlogState


def seo_node(state: BlogState):

    final_blog = optimize_seo(
        state["fact_checked_blog"]
    )

    return {
        "final_blog": final_blog
    }
