from pydantic import BaseModel, Field
from typing import List
class MOFData(BaseModel):
    """Formatted response for crystal structure from an LLM """
    name: str = Field(default="", description="The name of the material")
    a: float = Field(default=0, description="The cell parameter a in Angstrom")
    b: float = Field(default=0, description="The cell parameter b in Angstrom")
    c: float = Field(default=0, description="The cell parameter c in Angstrom")
    alpha: float = Field(default=0, description="The angle alpha in degree")
    beta: float = Field(default=0, description="The angle beta in degree")
    gamma: float = Field(default=0, description="The angle gamma in degree")
    ccdc_number: int = Field(default=0, description="The CCDC number of the material")
    other_names: List[str] = Field(default=[], description="Other names of the material mentioned in the text")

class MOFCollection(BaseModel):
    """Formatted response for material data from an LLM """
    materials: List[MOFData] = Field(default=[], description="The list of materials")