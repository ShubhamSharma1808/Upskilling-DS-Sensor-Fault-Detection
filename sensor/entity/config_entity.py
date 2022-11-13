from datetime import datetime
import os
from sensor.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()) -> None:
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = training_pipeline.ARTIFACT_DIR    
        self.timestamp = timestamp


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
