from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    """
    Extracts text from a given PDF file.

    Args:
        file: A file object representing the PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"An error occurred while reading the PDF: {e}")