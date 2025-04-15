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
        self.final_model_dir=os.path.join("final_model")


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

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transform_data:str=os.path.join(
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
        )
        self.transform_data_train:str=os.path.join(
            self.transform_data,training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_PATH.replace('csv','npy')
        )
        
        self.transform_data_test:str=os.path.join(
            self.transform_data,training_pipeline.DATA_TRANSFORMATION_TEST_FILE_PATH.replace('csv','npy')
        )

        self.data_transform_object:str=os.path.join(
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
        )
        self.data_transform_object_file_path:str=os.path.join(
            self.data_transform_object,training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
        )

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_train_path:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME
        )
        self.model_trained_path:str=os.path.join(
            self.model_train_path,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
        )
        self.model_file_path:str=os.path.join(
            self.model_trained_path,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.model_expected_score:float=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.model_OF_UF_threshold:float=training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD          