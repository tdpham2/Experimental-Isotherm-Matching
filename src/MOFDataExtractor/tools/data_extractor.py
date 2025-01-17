from langchain.tools import tool
import os
from langchain_openai import ChatOpenAI
from MOFDataExtractor.models.MOFCrystalData import *

@tool
def convert_pdfs_to_text(path_to_pdfs):
    """Convert all PDF files in a directory to a single text string.

    This function reads all PDF files in the specified directory and combines
    their text content into a single string. It handles errors gracefully by
    skipping files that cannot be processed.

    Args:
        path_to_pdfs (str): Path to the directory containing PDF files.

    Returns:
        str: Combined text content from all successfully processed PDF files.

    Raises:
        None: Exceptions are caught and printed, but not raised.
    """
    import PyPDF2
    
    def extract_text(page):
        text = page.extract_text()
        return text
    
    combined_text = ""
    for filename in os.listdir(path_to_pdfs):
        if filename.endswith(".pdf"):
            file_path = os.path.join(path_to_pdfs, filename)
            try:
                reader = PyPDF2.PdfReader(file_path)
                text = [extract_text(page) for page in reader.pages]
                combined_text += " ".join(text)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
    return combined_text


    