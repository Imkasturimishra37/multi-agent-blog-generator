from config import llm


def review_blog(blog):

    prompt = f"""
    You are an expert blog editor.

    Review the following blog.

    Improve:

    - Grammar
    - Sentence structure
    - Readability
    - Professional tone
    - Remove repeated sentences

    Do not change the meaning.

    Blog:

    {blog}
    """

    response = llm.invoke(prompt)

    return response.content