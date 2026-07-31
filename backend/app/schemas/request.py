from pydantic import BaseModel

class TestRequest(BaseModel):
    company : str
    position : str
    description : str
    responsibilities : str | None
    requirements : str
    salary : str | None
    company_description : str | None
    miscellaneous_benefits : str | None
    days_opened : int
    post_on_website : bool
    hiring_timeline : bool
    hiring_manager_listed : bool