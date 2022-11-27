from sensor.exception import Sensor_Exception
from sensor.logger import logging
from sensor.configs.mongo_db_Connection import MongoDBClient

import numpy as np
import pandas as pd
import sys


class SensorData:
    '''This class helps to export entire mongoDB record as pandas dataframe'''
    
    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient()
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    def export_collection_as_dataframe(self, collection_name, database_name = None)-> pd.DataFrame:
        try:
            # export entire collection as dataframe
            # return pd.DataFrame of collection
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find())) 
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)          
                   
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
        return df
