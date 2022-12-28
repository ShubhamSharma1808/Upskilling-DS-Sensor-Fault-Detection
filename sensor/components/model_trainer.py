from sensor.logger import logging
from sensor.exception import Sensor_Exception
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.utils.main_utils import load_numpy_array_data
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.utils.main_utils import load_object, save_object
from sensor.ml.model.estimator import SensorModel

import sys
import numpy as np

class ModelTrainer:
    
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact) -> None:
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise Sensor_Exception(e, sys)        
        
    def perform_hyper_parameter_tuning(self):...
    
    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise Sensor_Exception(e, sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            
            # loading train and test array.
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                np.delete(train_arr, -1, 1),                # without last column
                np.delete(train_arr, slice(0,-1), axis=1),  # only last column
                np.delete(test_arr, -1, 1),                 # without last column
                np.delete(test_arr, slice(0,-1), axis=1)    # only last column
            )
            
            model = self.train_model(x_train, y_train)
            
            y_train_pred = model.predict(x_train)
            classification_train_metric =  get_classification_score(y_true=y_train, y_pred=y_train_pred)
            
            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception(f"Trained model f1_score({classification_train_metric.f1_score}) is below than expected accuracy({self.model_trainer_config.expected_accuracy})")
            
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            
            # Check for Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            
            if diff > self.model_trainer_config.overfitting_underfitting_threshold :
                raise Exception(f"f1_score diff({diff}) b/w train & test is higher than Underfitting/Overfitting threshold ({self.model_trainer_config.overfitting_underfitting_threshold })")
                
            # getting the preprocessor created and used in Data Transformation step and 
            # saving it with the model created above in a SensorModel Class oject.
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)                
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)
            
            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path, 
                train_metric_artifact = classification_train_metric,
                test_metric_artifact = classification_test_metric)
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
                        
            return model_trainer_artifact
            
        except Exception as e:
            raise Sensor_Exception(e, sys)