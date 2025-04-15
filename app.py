import os
import sys

from dotenv import load_dotenv
import pymongo.mongo_client
load_dotenv()
MONGO=os.getenv('MONGO_DB_URL')
print(MONGO)

import pymongo
import certifi
ca=certifi.where()

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI ,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client=pymongo.mongo_client.MongoClient(host=MONGO)

from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from networksecurity.utils.main_utils.ml_utils.model.estimator import NetworkModel

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Note: 'allow_origins' (not 'allow_origin')
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/',tags={'authentication'})
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.inititate_training_pipeline()
        return Response("Training Sucessfull")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        print(df)
        #df=df.drop(['Result'],axis=1)
        preprocesor=load_object("final_model/preprocess.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)



if __name__=='__main__':
    app_run(app,host='0.0.0.0',port=8000)