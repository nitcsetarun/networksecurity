import os
import sys
import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.data_artifacts import DataValidationArtifacts,DataTransformationArtifacts
from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import save_object,save_to_np



class DataTransformation:
    def __init__(self,data_validation_arifacts:DataValidationArtifacts,data_transformation_config:DataTransformationConfig):
        try:

            self.data_validation_artifacts=data_validation_arifacts
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transform_object(cls)->Pipeline:
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)    



    def initiate_transformation(self)->DataTransformationArtifacts:
        try:
            train_data_path=self.data_validation_artifacts.valid_train_path
            test_data_path=self.data_validation_artifacts.valid_test_path

            train_data=DataTransformation.read_data(train_data_path)
            test_data=DataTransformation.read_data(test_data_path)

            input_feature_train=train_data.drop([TARGET_COLUMN],axis=1)
            target_feature_train=train_data[TARGET_COLUMN]
            target_feature_train=target_feature_train.replace(-1,0)
            
            input_feature_test=test_data.drop([TARGET_COLUMN],axis=1)
            target_feature_test=test_data[TARGET_COLUMN]
            target_feature_test=target_feature_test.replace(-1,0)
            

            preprocessor=self.get_data_transform_object()
            pre_processor_object=preprocessor.fit(input_feature_train)
            transformed_input_train_feature=pre_processor_object.transform(input_feature_train)
            transformed_input_test_feature=pre_processor_object.transform(input_feature_test)

            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test)]

            save_to_np(self.data_transformation_config.transform_data_train,array=train_arr)
            save_to_np(self.data_transformation_config.transform_data_test,array=test_arr)
            save_object(self.data_transformation_config.data_transform_object_file_path,obj=pre_processor_object)

            data_transformation_artifacts=DataTransformationArtifacts(
                
                        transformed_object_path=self.data_transformation_config.data_transform_object_file_path,
                        transformed_train_path=self.data_transformation_config.transform_data_train,
                        transformed_test_path=self.data_transformation_config.transform_data_test

            )

            return data_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
            

