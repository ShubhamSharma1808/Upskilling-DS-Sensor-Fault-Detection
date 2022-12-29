from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from sensor.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact
from sensor.exception import Sensor_Exception
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
from sensor.constants.s3_bucket import TRAINING_BUCKET_NAME
from sensor.constants.training_pipeline import SAVED_MODELS_DIR
from sensor.cloud_storage.s3_syncer  import S3Sync
import sys, os

class TrainPipeline:
    
    is_training_pipeline = False
    def __init__(self) -> None:
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        
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
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Validation")
            data_validation = DataValidation( self.data_validation_config, data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)
            
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Transformation")
            data_transformation = DataTransformation(
                data_transformation_config=self.data_transformation_config, 
                data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Model Trainer")
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    
    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact, data_validation_artifact: DataValidationArtifact) -> ModelEvaluationArtifact:
        try:
            self.model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Model Evalutaion")
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                model_trainer_artifact=model_trainer_artifact,
                data_validation_artifact=data_validation_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            self.model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Model Pusher")
            model_evaluation = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_evaluation.initiate_model_pusher()
            logging.info(f"Model Pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)

    def sync_artifact_dir_to_s3(self,):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_from_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise Sensor_Exception(e, sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODELS_DIR}"
            self.s3_sync.sync_folder_from_s3(folder=SAVED_MODELS_DIR, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise Sensor_Exception(e, sys)

    def run_pipeline(self):
        try:
            TrainPipeline.is_training_pipeline = True
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(
                model_trainer_artifact=model_trainer_artifact, 
                data_validation_artifact=data_validation_artifact)
            if model_evaluation_artifact.is_model_accepted == True:
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            else:
                raise Exception("Trained model is not accepted.")
            TrainPipeline.is_training_pipeline = False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_training_pipeline = False
            raise Sensor_Exception(e, sys)

