from sensor.constants import training_pipeline
from sensor.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import Sensor_Exception
from sensor.logger import logging
import pandas as pd
import numpy as np
import os, sys
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils import main_utils

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek

class DataTransformation:
    
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact) -> None:
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            logging.info("Entered get_data_transformer_object method of DataTransformation class")
            
            robust_scaler = RobustScaler()            
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            
            logging.info("Initialized Robust_Scaler and simple_imputer")
            
            preprocessor = Pipeline(steps=[("Imputer", simple_imputer), ("RobustScaler", robust_scaler)])
            
            logging.info("Created Preprocessor object from ColumnTransformer")            
            logging.info("Exiting get_data_transfomer_object method of DataTransformation class")
            
            return preprocessor
        
        except Exception as e:
            raise Sensor_Exception(e, sys)           
            
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:            
            #read the data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            #divide the train dataframe
            input_feature_train_df = train_df.drop(columns=[training_pipeline.TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[training_pipeline.TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            logging.info("Got input and target feature of Training Dataset")
            
            #divide the test dataframe
            input_feature_test_df = test_df.drop(columns=[training_pipeline.TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[training_pipeline.TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())
            logging.info("Got input and target feature of Testing Dataset")
            
            #Applying preprocessing object on  training and testing input features
            logging.info("Applying preprocessing object on  training and testing input features")
            preprocessor = self.get_data_transformer_object()
            input_feature_train_array = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor.transform(input_feature_test_df)
            
            #Applying SMOTETomek on training and testing dataset
            logging.info("Applying SMOTETomek on training and testing dataset")
            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_array, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_array, target_feature_test_df)
            
            #Created Train and Test array
            logging.info("Created Train and Test array")
            train_arr = np.c_[input_feature_train_final, target_feature_train_final]
            test_arr = np.c_[input_feature_test_final, target_feature_test_final]
            
            #saving the objects, train and test data
            main_utils.save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            main_utils.save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            main_utils.save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            
            return data_transformation_artifact         
           
        except Exception as e:
            raise Sensor_Exception(e,sys)