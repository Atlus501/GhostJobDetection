from pydantic import BaseModel
from datetime import datetime, timezone

class DataEntry(BaseModel):
    ghost_job : bool
    company : str
    position : str
    vagueness_score: float
    salary_present : bool
    days_opened : int
    post_on_website : bool
    hiring_timeline : bool
    hiring_manager_listed : bool
    created_date : datetime = datetime.now(timezone.utc)

class Predictors(BaseModel):
    vagueness_score: float
    salary_present : bool
    days_opened : int
    post_on_website : bool
    hiring_timeline : bool
    hiring_manager_listed : bool