from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
import logging 

from config.settings import settings

"""
Class for managing the MongoDB instance
"""
class MongoDB:
    """
    Constructor for the MongoDB manager.
    Params: None
    """
    def __init__ (self, table="GhostJobInfo", app_name="JobInfo"):
        db_username = settings.MONGODB_USERNAME
        db_password = settings.MONGODB_PASSWORD
        uri = f"mongodb+srv://{db_username}:{db_password}@jobinfo.hruhw82.mongodb.net/?appName={app_name}"
        self.client = AsyncMongoClient(uri, server_api=ServerApi('1'))
        self.logger = logging.getLogger(__name__)
        self.app_name = app_name
        self.table = table

    """
    Function for setting up indices 
    """
    async setup_index(self, indicies : list[str]):
        indicies = [(index, 1) for index in indices]
        await self.table.create_index(indicies, unique=True)

    """
    Function for getting the table that one is using
    Params: table (str) -- name of the table
    Returns: table object 
    """
    def get_collection(self):
        db = self.client[self.app_name]
        return db[self.table]

    """
    Asynchronous function to save data entries into the database 
    """
    async def upsert(self, query, data : dict):
        table = self.get_collection()

        try:
            update_data = {"$set": data}
            res = await table.update_one(query, update_data, upsert=True)
            return res
        except Exception as e:
            message = "An unexpected error occured while saving data."
            self.logger.error(f"{message} {str(e)}") 
            raise RuntimeError(message)