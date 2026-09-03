from config import llm


def optimize_seo(blog):

    prompt = f"""
    You are an SEO expert.

    Optimize the following blog.

    Tasks:

    1. Create an SEO-friendly title.
    2. Generate a meta description (max 160 characters).
    3. Suggest 5 SEO keywords.
    4. Improve headings if required.
    5. Return the complete optimized blog.

    Blog:

    {blog}
    """

    response = llm.invoke(prompt)

    return response.content
