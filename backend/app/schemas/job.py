from pydantic import BaseModel

"""
Class that hold job information for LLM analysis
"""
class Job(BaseModel):
  company : str
  position : str
  description : str
  responsibilities : str | None
  requirements : str
  salary : str
  company_description : str | None
  miscellaneous_benefits : str | None