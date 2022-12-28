from sensor.configs.mongo_db_Connection import MongoDBClient
from sensor.exception import Sensor_Exception
from sensor.pipeline.training_pipeline import TrainPipeline
import sys, warnings, os

from fastapi import FastAPI
from sensor.constants.application import APP_HOST, APP_PORT
from sensor.constants.training_pipeline import SAVED_MODELS_DIR
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import read_yaml_file, load_object
from uvicorn  import run as app_run


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        if train_pipeline.is_training_pipeline == True:
            return Response("Training Pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training Successfull !!")
    except Exception as e:
        return Response(f"Error occurred {e}")

@app.get("/predict")
async def predict_route():      # Function not completed
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None
        model_resolver = ModelResolver(model_dir=SAVED_MODELS_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
    except Exception as e:
        return Response(f"Error occurrred {e}")

def set_env_variable(env_file_path: str):
    env_config = read_yaml_file(file_path=env_file_path)
    os.environ['MONGO_DB_URL'] = env_config['MONGO_DB_URL'] 
    

def main():    
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        raise e    

if __name__ == '__main__':

    warnings.filterwarnings('ignore')
    app_run(app, host=APP_HOST, port=APP_PORT)
    
    
