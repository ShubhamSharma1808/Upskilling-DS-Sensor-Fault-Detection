from sensor.constants import training_pipeline
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import Sensor_Exception
from sensor.logger import logging
import pandas as pd
import os, sys
from scipy.stats import ks_2samp
from sensor.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    
    def validate_number_of_columns(self, sensor_Dataframe: pd.DataFrame) -> bool:
        try:
            schema_columns = self.schema_config["columns"]
            logging.info(f"no. of columns in the dataframe {len(sensor_Dataframe.columns)}")
            logging.info(f"No. of Schema columns : {len(schema_columns)}")
            logging.info(sensor_Dataframe.columns)
            if len(sensor_Dataframe.columns) == len(schema_columns):
                return True
            return False
        except Exception as e:
            raise Sensor_Exception(e,sys)
            
    def is_numerical_column_exist(self, sensor_Dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self.schema_config["numerical_columns"]
            dataframe_columns = sensor_Dataframe.columns
            
            missing_numerical_column = []
            missing_numerical_flag = False
            for column in numerical_columns:
                if column not in dataframe_columns:
                    missing_numerical_flag = True
                    missing_numerical_column.append(column)
            
            logging.info(f"Missing Numerical columns: [{missing_numerical_column}]")
            return  missing_numerical_flag    
        except Exception as e:
            raise Sensor_Exception(e,sys)
        
    '''
    You can have many more validations like say having validation on columns which have 0 standard deviation
    since it won't help in getting any info from that column since it's constant.
    '''
        
    def validate_columns_with_std_dev_zero(self, sensor_Dataframe: pd.DataFrame) -> None:
        try:
            pass
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05) -> bool:
        try:
            drift_status = False
            drift_report = {}            
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dict = ks_2samp(d1, d2)
                if is_same_dict.pvalue < threshold:
                    drift_status = True
                    is_found = True
                else: 
                    is_found = False
                drift_report.update({column:{
                    "p_value" : float(is_same_dict.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path 
            
            #Create Directory and save drift report  
            write_yaml_file(file_path=drift_report_file_path, data=drift_report)   
                     
            return drift_status
        
        except Exception as e:
            raise Sensor_Exception(e,sys)    
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""
            
            # get the train and test data
            train_Dataframe = DataValidation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_Dataframe = DataValidation.read_data(self.data_ingestion_artifact.test_file_path)
            
            # validation on number of columns
            train_column_flag = self.validate_number_of_columns(sensor_Dataframe = train_Dataframe)
            if not train_column_flag:
                error_message = f"{error_message}Train dataframe does not contain all columns.\n "
            
            test_column_flag = self.validate_number_of_columns(sensor_Dataframe = test_Dataframe)
            if not test_column_flag:
                error_message = f"{error_message}Test dataframe does not contain all columns.\n "
            
            # validation on numerical column
            train_missing_Numerical_column_flag = self.is_numerical_column_exist(sensor_Dataframe = train_Dataframe)
            if train_missing_Numerical_column_flag:
                error_message = f"{error_message}Missing numerical columns.\n "
            
            test_missing_Numerical_column_flag = self.is_numerical_column_exist(sensor_Dataframe = test_Dataframe)
            if test_missing_Numerical_column_flag:
                error_message = f"{error_message}Missing numerical columns.\n "
            
            if len(error_message) > 0:
                raise Exception(error_message)
            
            #let's check data drift
            drift_status = self.detect_dataset_drift(train_Dataframe, test_Dataframe)
            
            '''
            we can have exception if drift is found and stop the pipeline
            But that's not always the need since with drift too we can get the accuracy with the model
            So, not stopping right now 
            '''
            #preparing Data Validation Artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            ) 
            
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact           
            
        except Exception as e:
            raise Sensor_Exception(e, sys)
            #Validate the number of columns
        
    