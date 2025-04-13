from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from datetime import datetime

import sys
import os
import pandas as pd

if __name__=='__main__':
    try:
        tpcobj=TrainingPipelineConfig()
        dtingconfig=DataIngestionConfig(tpcobj)
        dataingestion=DataIngestion(dtingconfig)
        artifacts=dataingestion.initiate_data_ingestion()

        print(artifacts)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
  
 