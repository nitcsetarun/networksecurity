from networksecurity.constants import training_pipeline
from datetime import datetime
import os
import sys



class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_dir:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.training_dir:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_dir:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME
        )
        self.test_train_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database=training_pipeline.DATA_INGESTION_DATABASE_NAME        

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir , training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.data_validated_dir:str=os.path.join(
            self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        self.data_invalidated_dir:str=os.path.join(
            self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.data_valid_train:str=os.path.join(
            self.data_validated_dir,training_pipeline.TRAIN_FILE_NAME
        )
        self.data_valid_test:str=os.path.join(
            self.data_validated_dir,training_pipeline.TEST_FILE_NAME
        )
        self.data_invalid_train:str=os.path.join(
            self.data_invalidated_dir,training_pipeline.TRAIN_FILE_NAME
        )
        self.data_invalid_test:str=os.path.join(
            self.data_invalidated_dir,training_pipeline.TRAIN_FILE_NAME
        )
        self.drift_report_dir: str = os.path.join(
                                self.data_validation_dir,
                        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR
        )

        self.drift_report_file_path: str = os.path.join(
                        self.drift_report_dir,
                    training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )
