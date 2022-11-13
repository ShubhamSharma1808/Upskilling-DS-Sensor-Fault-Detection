import pymongo
import sensor.constants.database as db
from sensor.exception import Sensor_Exception

class MongoDBClient:

    client = None    
    def __init__(self, database_name = db.DATABASE_NAME) -> None:    
        try:
            if  MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(db.DATABASE_CONNECTION_STRING)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name 
        except Exception as e:
            raise Sensor_Exception(e, sys)