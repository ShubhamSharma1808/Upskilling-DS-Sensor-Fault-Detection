import os,sys
import yaml
from sensor.exception import Sensor_Exception
import numpy as np
from sensor.logger import logging
import dill


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise Sensor_Exception(e, sys)
    
    
def write_yaml_file(file_path: str, data: object, replace: bool = False)-> None:    
    try:        
        if replace:            
            if os.path.exists(file_path):                
                os.remove(file_path)
                
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        
        with open(file_path, "w") as file:
            yaml.dump(data, file)
    
    except Exception as e:
        raise Sensor_Exception(e, sys) 
    
def save_numpy_array_data(file_path: str, array: np.array) -> None:
    try:        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise Sensor_Exception(e, sys)

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise Sensor_Exception(e, sys)
 
# Saving model as a pickle in file
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save object method of mainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)    #dill used for serialization/de-serialization
    except Exception as e:
        raise Sensor_Exception(e, sys)
        

