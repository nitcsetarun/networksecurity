from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.data_artifacts import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file



class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifacts:DataIngestionArtifacts):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e :
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(filepath)-> pd.DataFrame:
        try:
            
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def match_columns(self,data: pd.DataFrame)-> bool:
        try:
            number_of_column=(len(self._schema_config))
            logging.info(f'Total Number Required{number_of_column}')
            logging.info(f'Total Number of columns in data : {len(data.columns)}')
            if number_of_column == len(data.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)   

    def check_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    isFound=False
                else:
                    isFound=True
                    status=False
                report.update({column:{
                    'p_value':is_same_dist.pvalue,
                    'is_found':isFound
                }})
            
            
            write_yaml_file(self.data_validation_config.drift_report_dir,self.data_validation_config.drift_report_file_path,report)
            return status


        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def data_validation_inititate(self)-> DataValidationArtifacts:
        try:
            train_data_path=self.data_ingestion_artifacts.training_file_path
            test_data_path=self.data_ingestion_artifacts.testing_file_path

            train_data=DataValidation.read_data(train_data_path)
            test_data=DataValidation.read_data(test_data_path)

            status=self.match_columns(train_data)
            if not status:
                error_message='Train data doesnot contains all columns'

            status=self.match_columns(test_data)
            if not status:
                error_message='Test data doesnot contaions all columns'

            status=self.check_drift(base_df=train_data,current_df=test_data)
            
            train_valid_path=self.data_validation_config.data_valid_test
            trdir=os.path.dirname(train_valid_path)
            os.makedirs(trdir,exist_ok=True)

            train_data.to_csv(train_valid_path,index=False,header=True)

            test_valid_path=self.data_validation_config.data_valid_test
            tsdir=os.path.dirname(test_data_path)
            os.makedirs(tsdir,exist_ok=True)
            test_data.to_csv(test_valid_path,index=False,header=True)

            datavalidationartifacts=DataValidationArtifacts(
                    validation_status=status,
                    valid_train_path=self.data_validation_config.data_valid_train,
                    valid_test_path=self.data_validation_config.data_valid_test,
                    invalid_train_path=None,
                    invalid_test_path=None,
                    drift_file_path=self.data_validation_config.drift_report_dir

            )


            return datavalidationartifacts



        except Exception as e:
            raise NetworkSecurityException(e,sys)
