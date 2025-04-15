from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.cloud.aws_s3_syncer import S3syncer
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig
)

from networksecurity.entity.data_artifacts import(
    DataIngestionArtifacts,DataValidationArtifacts,DataTransformationArtifacts,ClassificationMetricsArtifacts,ModelTrainerArtifacts
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline=TrainingPipelineConfig()
        self.s3_syncer=S3syncer()

    def data_ingestion(self):
        try:
            data_ingestion_config=DataIngestionConfig(self.training_pipeline)
            logging.info("Data Ingestion Started")
            data_ingestion=DataIngestion(data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed Artifacts Created")
            return data_ingestion_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def data_validation(self,data_ingestion_artifacts:DataIngestionArtifacts):
        try:
            data_validation_config=DataValidationConfig(self.training_pipeline)
            logging.info("Data Transformation Started")
            data_validation=DataValidation(data_validation_config,data_ingestion_artifacts)
            data_validation_artifacts=data_validation.data_validation_inititate()
            logging.info("Data validation Completed Artifacts Created")
            return data_validation_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def data_transformation(self,data_validation_artifacts : DataValidationArtifacts):
        try:
            data_transformation_config=DataTransformationConfig(self.training_pipeline)
            logging.info("Data Transformation Started")
            data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
            data_transformation_artifacts=data_transformation.initiate_transformation()
            logging.info("Data Transformation Completed")
            return data_transformation_artifacts
        except Exception as e:
            raise  NetworkSecurityException(e,sys)

    def ModelTrainer(self,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            model_trainer_config=ModelTrainerConfig(self.training_pipeline)
            logging.info("Training Started")
            model_trainer=ModelTrainer(data_transformation_artifacts,model_trainer_config)
            model_trainer_artifacts=model_trainer.inititate_model_training()
            logging.info("Model Training Completed , Artifacts  Created")
            return model_trainer_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def artifact_to_s3(self):
        try:
            
            s3_bucket_url=f's3://{TRAINING_BUCKET_NAME}/artifacts/{self.training_pipeline.timestamp}'
            artifacts_folder=self.training_pipeline.artifact_dir
            self.s3_syncer.sync_folder_to_s3(artifacts_folder,s3_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def model_to_s3(self):
        try:
            s3_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline.timestamp}"
            model_folder=self.training_pipeline.final_model_dir
            self.s3_syncer.sync_folder_to_s3(model_folder,s3_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)            
             

    def inititate_training_pipeline(self):
        try:
            data_ingestion_artifacts=self.data_ingestion()
            data_validation_artifacts=self.data_validation(data_ingestion_artifacts)
            data_transformation_artifacts=self.data_transformation(data_validation_artifacts)
            model_trainer_artifacts=self.ModelTrainer(data_transformation_artifacts)

            self.artifact_to_s3()
            self.model_to_s3()

            return model_trainer_artifacts

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)                   