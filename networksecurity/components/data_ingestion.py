import pymongo.mongo_client
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import os
import sys
from typing import List
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pymongo

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.data_artifacts import DataArtifacts

from dotenv import load_dotenv
load_dotenv()
MONGO=os.getenv("MONGO_DB_URL")




class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_from_mongo(self):
        try:
            database_name=self.data_ingestion_config.database
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.mongo_client.MongoClient(MONGO)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(collection.find())
            if '_id' in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            df.replace({'na':np.nan},inplace=True)    

            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def store_to_featurepath(self,dataframe:pd.DataFrame):
        try:
            feature_path=self.data_ingestion_config.feature_store_dir
            dir=os.path.dirname(feature_path)
            os.makedirs(dir,exist_ok=True)
            print(feature_path)
            dataframe.to_csv(feature_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_test_train(self,dataframe:pd.DataFrame):
        try:
            #df=pd.read_csv(self.data_ingestion_config.feature_store_dir)
            train,test=train_test_split(dataframe,test_size=self.data_ingestion_config.test_train_split_ratio)
            logging.info("Performing Test train Split")
            logging.info("Exiting Train est split and creating directory")

            train_dir=os.path.dirname(self.data_ingestion_config.training_dir)
            test_dir=os.path.dirname(self.data_ingestion_config.testing_dir)

            os.makedirs(train_dir,exist_ok=True)
            train.to_csv(self.data_ingestion_config.training_dir,index=False,header=True)
            logging.info("Training set saved")

            os.makedirs(test_dir,exist_ok=True)
            test.to_csv(self.data_ingestion_config.testing_dir,index=False,header=True)

            



        except Exception as e:
            raise NetworkSecurityException(e,sys)        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_from_mongo()
            dataframe=self.store_to_featurepath(dataframe)
            self.split_test_train(dataframe)
            data_artifacts=DataArtifacts(training_file_path=self.data_ingestion_config.training_dir,testing_file_path=self.data_ingestion_config.testing_dir)

            return data_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)    

