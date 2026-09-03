from agents.review_agent import review_blog
from state.blog_state import BlogState


def review_node(state: BlogState):

    reviewed = review_blog(
        state["blog"]
    )

    return {
        "reviewed_blog": reviewed
    }
