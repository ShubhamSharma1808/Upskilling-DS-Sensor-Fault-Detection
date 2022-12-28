from sensor.logger import logging
from sensor.exception import Sensor_Exception
from sensor.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from sensor.entity.config_entity import ModelPusherConfig

import os, shutil

class ModelPusher:
    
    def __init__(self, 
                 model_evaluation_artifact: ModelEvaluationArtifact, 
                 model_pusher_config: ModelPusherConfig) -> None:
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
        
    def initiate_model_pusher(self, ) -> ModelPusherArtifact:
        
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            #creating model pusher dir to save model            
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            
            #save model in saved model dir
            saved_model_path = self.model_pusher_config.saved_model_dir
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
            
            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)