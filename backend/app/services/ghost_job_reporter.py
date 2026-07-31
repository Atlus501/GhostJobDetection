from schemas.model import DataEntry

"""
Class for reporting ghost jobs incidents
"""
class GhostJobReporter:
    def __init__ (self, db):
        self.db = db

    """
    Function for reporting ghost jobs
    """
    async def report(self, job : DataEntry):
        res = await self.db.upsert({"company" : job.company, "position" : job.position}, entry=job.model_dump())
        return res