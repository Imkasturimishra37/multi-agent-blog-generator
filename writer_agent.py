from config import llm


def generate_blog(research_data, outline):

    prompt = f"""
    You are a professional blog writer.

    Topic:
    {research_data["topic"]}

    Research Summary:
    {research_data["research_summary"]}

    Blog Outline:
    {outline}

    Write a professional, engaging, SEO-friendly blog.

    Requirements:
    - Follow the outline strictly.
    - Use proper headings.
    - Write in simple English.
    - Add examples where appropriate.
    - Do not invent facts.
    - End with a conclusion.
    """

    response = llm.invoke(prompt)

    return response.content
