from sensor.exception import Sensor_Exception
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from pandas import DataFrame

from sensor.data_access.sensor_data import SensorData
import sys,os

class DataIngestion:
    
    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:  
            raise Sensor_Exception(e, sys)
        
    '''
    Export Mongo DB Collection into feature store
    '''
    def export_data_into_feature_Store(self) -> DataFrame:
        try:
            logging.info("Exporting data from Mongo DB to feature store")
            sensor_data = SensorData()
            sensor_dataframe = sensor_data.export_collection_as_dataframe(self.data_ingestion_config.collection_name)
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            sensor_dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return sensor_dataframe          
            
        except Exception as e:
            raise Sensor_Exception(e, sys)
    
    
    def split_data_as_train_test(self, dataframe:DataFrame)-> None:
        pass
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            sensor_Dataframe = self.export_data_into_feature_Store()
            self.split_data_as_train_test(sensor_Dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)