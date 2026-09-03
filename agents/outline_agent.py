from config import llm


def generate_outline(research_data, feedback=""):

    prompt = f"""
    You are an expert blog planner.

    Topic:
    {research_data["topic"]}

    Research Summary:
    {research_data["research_summary"]}

    User Feedback:
    {feedback}

    Create a professional blog outline.

    Requirements:

    - Follow the research summary.
    - If feedback is provided, improve the outline accordingly.
    - Include:
      1. Blog Title
      2. Introduction
      3. Main Headings
      4. Sub Headings
      5. Conclusion
      6. FAQs

    Return only the outline.
    """

    response = llm.invoke(prompt)

    return response.content
