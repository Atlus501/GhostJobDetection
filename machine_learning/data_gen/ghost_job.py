from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
import logging 

from config.mongodb import mongodb_config
from data_gen.schemas import data_entry

"""
Class for managing the MongoDB instance
"""
class GhostJobDB:
    """
    Constructor for the MongoDB manager.
    Params: None
    """
    def __init__ (self, table="GhostJobInfo"):
        db_username = mongodb_config.MONGODB_USERNAME
        db_password = mongodb_config.MONGODB_PASSWORD
        uri = f"mongodb+srv://{db_username}:{db_password}@jobinfo.hruhw82.mongodb.net/?appName=JobInfo"
        self.client = AsyncMongoClient(uri, server_api=ServerApi('1'))
        self.logger = logging.getLogger(__name__)
        self.table = table

    """
    Function for getting the table that one is using
    Params: table (str) -- name of the table
    Returns: table object 
    """
    def get_collection(self):
        db = self.client["JobInfo"]
        return db[self.table]

    """
    Function for setting up indices 
    """
    async def setup_index(self, indicies : list[str]):
        indicies = [(index, 1) for index in indicies]
        collection = self.get_collection()
        await collection.create_index(indicies, unique=True)

    """
    Asynchronous function to save data entries into the database 
    """
    async def save(self, id : int | None, entry : data_entry):
        table = self.get_collection()

        try:
            query = {"_id": id} if id is not None else {}
            update_data = {"$set": entry.model_dump()}
            res = await table.update_one(query, update_data, upsert=True)
            return res
        except Exception as e:
            message = "An unexpected error occured while saving data."
            self.logger.error(f"{message} {str(e)}") 
            raise RuntimeError(message)

    """
    Asyncrhonous function to load data entires into the database
    """
    async def load(self, limit=None):
        table = self.get_collection()

        try:
            cursor = table.find({}).limit(limit)
            docs = await cursor.to_list()
            return docs
        except Exception as e:
            message = "An unexpected error occured retrieving data."
            self.logger.error(f"{message} {str(e)}") 
            raise RuntimeError(message)

    """
    Asynchronous function to update data entries
    """
    async def delete(self, id : int):
        table = self.get_collection()

        try:
            res = await table.delete_one({"_id":id})
            return res
        except Exception as e:
            message = "An unexpected error occured deleting data."
            self.logger.error(f"{message} {str(e)}") 
            raise RuntimeError(message)