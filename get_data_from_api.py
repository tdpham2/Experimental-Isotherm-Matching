from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class MOFCrystalData(BaseModel):
    """Formatted response for crystal structure from an LLM """
    
    a: float = Field(default=0, description="The cell parameter a in Angstrom")
    b: float = Field(default=0, description="The cell parameter b in Angstrom")
    c: float = Field(default=0, description="The cell parameter c in Angstrom")
    alpha: float = Field(default=0, description="The angle alpha in degree")
    beta: float = Field(default=0, description="The angle beta in degree")
    gamma: float = Field(default=0, description="The angle gamma in degree")
    ccdc_number: str = Field(default="", description="The CCDC number of the material")

class MOFDataExtractor:
    def __init__(self,model_name="gpt-4o-mini",api_key=None,temperature=0):
        llm = ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
        self.llm = llm

    def run(self, query):
        structured_llm = self.llm.with_structured_output(MOFCrystalData)
        messages = structured_llm.invoke(query)
        return messages
