import os
import sys
import json

from dotenv import load_dotenv
import pymongo.database
import pymongo.mongo_client

load_dotenv()

MONGO=os.getenv("MONGO_DB_URL")
print(MONGO)

import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,filepath):
        try:
            self.filepath=filepath
            data=pd.read_csv(self.filepath)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_mongoDB(self,record,database,collection):
        try:
            self.record=record
            self.collection=collection
            self.database=database

            self.mongo_client=pymongo.mongo_client.MongoClient(MONGO)
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.record)

            return (len(self.record))

        except Exception as e:
            raise NetworkSecurityException(e,sys)        

if __name__=='__main__':
    FILE_PATH="Network_data\phisingData.csv"
    DATABASE='TARUN_MLOPS'
    COLLECTION='Network_security'

    NetworkDataExtractobj=NetworkDataExtract()
    records=NetworkDataExtractobj.csv_to_json(FILE_PATH)
    len_ofRecords=NetworkDataExtractobj.insert_mongoDB(records,DATABASE,COLLECTION)

    print(len_ofRecords)
