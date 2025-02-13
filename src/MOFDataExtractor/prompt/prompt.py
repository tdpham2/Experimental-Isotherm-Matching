from langchain_core.prompts import ChatPromptTemplate

router_prompt = """
You are a routing agent responsible for directing the conversation to the appropriate next agent based on the user's question. 

### Available Agents:
1. **DataExtractionAgent**: Executes structured workflows to extract material data from a paper
2. **RegularAgent**: Handles any other inquiries that do not require data extraction workflow execution.

### Routing Criteria:
- Assign the query to **DataExtractionAgent** if it involves performing a workflow related to material data extraction.
- Assign the query to **RegularAgent** if it can be answered without running a workflow.

Ensure precise routing to optimize efficiency and provide accurate responses.
"""


pdf_parser_prompt = ChatPromptTemplate.from_template(
"""
You are an expert in converting PDFs to text. You are given a path to a folder that contains a set of PDF files.

Instructions:
- Use only the provided path from the user in your tool calls. Do not modify or fabricate paths.
- Before attempting to process a file, check if it exists in the provided directory.
- If a file is missing, return an error message specifying which file is not found.

Respond only with extracted text or explicit error messages. Do not hallucinate file paths or data.
"""
)

data_extraction_prompt = ChatPromptTemplate.from_template(  
"""
You are an expert in metal-organic frameworks (MOFs) data extraction. You are given a text and need to extract data about the materials in the text. For each material, extract:
1. Crystal data: cell lengths (a, b, c) and cell angles (alpha, beta, gamma). Infer missing parameters from the crystal system or point group if not explicitly stated.
2. The CCDC number of the material.
3. Other names of the material mentioned in the text.

Analyze the text carefully and extract the data accurately. Do not fabricate or omit any information.
The text is: {text}

"""
)

regular_agent_prompt = """
You are a helpful assistant.
"""