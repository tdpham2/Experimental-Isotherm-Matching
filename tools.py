from langchain.tools import tool
import os

@tool
def compare_adsorbent_data(adsorbent_data: str, mof_data: str):
    """Compare the adsorbent data with the MOF data"""
    return adsorbent_data == mof_data

@tool
def setup_graspa_simulation(adsorbent_data: str, mof_data: str):
    return True

@tool
def convert_pdfs_to_text(path_to_pdfs):
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