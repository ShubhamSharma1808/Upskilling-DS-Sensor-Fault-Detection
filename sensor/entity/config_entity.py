from datetime import datetime
import os
from sensor.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()) -> None:
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = training_pipeline.ARTIFACT_DIR    
        self.timestamp = timestamp

''' It contains the constants, needed for data ingestion component for storing artifacts (feature store, training and testing data)'''
class DataIngestionConfig:
    
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:

        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)

        self.training_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)

        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        
        self.valid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)        
        self.invalid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        
        self.valid_train_file_path = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)        
        self.valid_test_file_path = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)        
        self.invalid_test_file_path = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)        
              
        self.drift_report_file_path = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        
class DataTransformationConfig:
    
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))        
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,  training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
        
        

