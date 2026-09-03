from langgraph.graph import StateGraph, END

from state.blog_state import BlogState

from nodes.research_node import research_node
from nodes.outline_node import outline_node
from nodes.writer_node import writer_node
from nodes.review_node import review_node
from nodes.fact_checker_node import fact_checker_node
from nodes.seo_node import seo_node


workflow = StateGraph(BlogState)

workflow.add_node("Research", research_node)
workflow.add_node("Outline", outline_node)
workflow.add_node("Writer", writer_node)
workflow.add_node("Review", review_node)
workflow.add_node("FactChecker", fact_checker_node)
workflow.add_node("SEO", seo_node)

workflow.set_entry_point("Research")

workflow.add_edge("Research", "Outline")
workflow.add_edge("Outline", "Writer")
workflow.add_edge("Writer", "Review")
workflow.add_edge("Review", "FactChecker")
workflow.add_edge("FactChecker", "SEO")
workflow.add_edge("SEO", END)

graph = workflow.compile()