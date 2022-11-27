from sensor.exception import Sensor_Exception
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sensor.data_access.sensor_data import SensorData
import sys,os
from sensor.utils.main_utils import read_yaml_file
from sensor.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH

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
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
 
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise Sensor_Exception(e, sys)
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            sensor_Dataframe = self.export_data_into_feature_Store()
            
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
            '''through EDA we have got columns that needs to be dropped (we have stored them in Schema.yaml file)'''
            ''' this needs to be checked how to do this'''
            sensor_Dataframe = sensor_Dataframe.drop(_schema_config[SCHEMA_DROP_COLS], axis=1)
            
            logging.info("Got the data from the DB")
                        
            self.split_data_as_train_test(sensor_Dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path = self.data_ingestion_config.training_file_path, 
                test_file_path = self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise Sensor_Exception(e, sys)
        