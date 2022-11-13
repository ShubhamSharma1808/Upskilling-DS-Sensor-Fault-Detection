from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.exception import Sensor_Exception
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
import sys, os

class TrainPipeline:
    
    def __init__(self) -> None:
        training_pipeline_config = TrainingPipelineConfig()
        self.training_pipeline_config = training_pipeline_config
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config= self.training_pipeline_config)
            logging.info("Starting data ingestion")
            # calling data ingestion component
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise Sensor_Exception(e, sys)

