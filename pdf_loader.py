from pypdf import PdfReader


def load_pdf(file):

    """
    Reads a PDF file and returns all text.
    """

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text