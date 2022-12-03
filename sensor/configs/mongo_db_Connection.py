import pymongo
import sensor.constants.database as db
import certifi
from sensor.exception import Sensor_Exception

'''
Certifi is a set of root certificates.

There is no default certificate authority for the Python installation on OSX. A possible default is exactly the one provided by the certifi package.

After that, you just can create an SSL context that has the proper default as the following (certifi.where() gives the location of a certificate authority):
'''

ca = certifi.where()
    
class MongoDBClient:    
    client = None    
    def __init__(self, database_name = db.DATABASE_NAME) -> None:    
        try:
            if  MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(db.DATABASE_CONNECTION_STRING, tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name 
        except Exception as e:
            raise Sensor_Exception(e, sys)