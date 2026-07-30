from pydantic import BaseModel
from datetime import datetime, timezone

class data_entry(BaseModel):
    ghost_job : bool
    vagueness_score: float
    salary_present : bool
    days_opened : int
    post_on_website : bool
    hiring_timeline : bool
    hiring_manager_listed : bool
    created_date : datetime = datetime.now(timezone.utc)