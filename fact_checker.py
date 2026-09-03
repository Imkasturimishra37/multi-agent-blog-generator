from config import llm


def fact_check_blog(research_data, blog):

    prompt = f"""
    You are an expert fact checker.

    Research Summary:
    {research_data["research_summary"]}

    Blog:
    {blog}

    Your tasks:

    1. Compare the blog with the research summary.
    2. Remove unsupported claims.
    3. Correct factual mistakes.
    4. Keep the writing style unchanged.
    5. Return only the corrected blog.

    Do not add new information.
    """

    response = llm.invoke(prompt)

    return response.content