from langchain_core.prompts import ChatPromptTemplate

pdf_parser_prompt = ChatPromptTemplate.from_template(
"""
You are an expert in converting pdf to text. You are given a folder of pdfs and need to convert each pdf to text. Use your tools to do this.
"""
)

data_extraction_prompt = ChatPromptTemplate.from_template(  
"""
You are an expert in metal-organic framework (MOF) data extraction. You are given a text and need to extract data about the materials in the text. For each material, extract:
1. Crystal data: cell lengths (a, b, c) and cell angles (alpha, beta, gamma). Infer missing parameters from the crystal system or point group if not explicitly stated.
2. The CCDC number of the material.
3. Other names of the material mentioned in the text.

Analyze the text carefully and extract the data accurately. Do not fabricate or omit any information.
The text is: {text}

"""
)