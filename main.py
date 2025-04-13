


from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from networksecurity.entity.data_artifacts import DataIngestionArtifacts,DataValidationArtifacts
from datetime import datetime

import sys
import os
import pandas as pd

if __name__=='__main__':
    try:
        training_piperline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_piperline_config)
        dataingestion=DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion Initiated")
        data_ingestion_artifacts=dataingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(data_ingestion_artifacts)
        data_validation_config=DataValidationConfig(training_piperline_config)
        #data_ingestion_artifacts=DataIngestionArtifacts(data_ingestion_config)
        logging.info("Data Validation Started")
        datavalidation=DataValidation(data_validation_config,data_ingestion_artifacts)
        data_validation_artifacts=datavalidation.data_validation_inititate()
        logging.info('Data Validation completed')
        print(data_validation_artifacts)

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
  
 

