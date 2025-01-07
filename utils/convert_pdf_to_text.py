import os
from PyPDF2 import PdfReader
import subprocess
import nltk
nltk.download('punkt')

def extract_text(page):
    text = page.extract_text()
    return text

def convert_pdfs_to_text(folder_path):
    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                reader = PdfReader(file_path)
                text = [extract_text(page) for page in reader.pages]
                combined_text += " ".join(text)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
    return combined_text

def count_tokens(text):
    tokens = nltk.word_tokenize(text)
    return len(tokens)

# Specify the folder containing PDFs
basepath = '/home/tdpham/Dropbox/Northwestern/work/Experimental_isotherm_project/OpenAI/papers_storage'

dois = os.listdir(basepath)

for doi in dois:
    if not doi.startswith('10'):
        continue
    print(doi)
    folder_path = os.path.join(basepath, doi)
    combined_text = convert_pdfs_to_text(folder_path)
    os.mkdir(doi)
    with open(doi + '/' + 'combined_text.txt', 'w') as f:
        f.write(combined_text)

    total_tokens = count_tokens(combined_text)

    with open('token_counts', 'a') as f:
        f.write("{},{}\n".format(doi, total_tokens))
