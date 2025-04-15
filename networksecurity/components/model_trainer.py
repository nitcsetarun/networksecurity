from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import  logging

import os
import sys

#from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report,accuracy_score,precision_score,recall_score,f1_score

#from sklearn.ensemble import RandomForestClassifier

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.data_artifacts import ClassificationMetricsArtifacts,ModelTrainerArtifacts,DataTransformationArtifacts


from networksecurity.utils.main_utils.ml_utils.classification.classification import classification_report
from networksecurity.utils.main_utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_numpy_array,save_object,load_object,evaluateModel



from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow

from urllib.parse import urlparse

import dagshub
dagshub.init(repo_owner='nitcsetarun', repo_name='networksecurity', mlflow=True)




class ModelTrainer:
    def __init__(self,data_transformation_artifacts:DataTransformationArtifacts,model_trainer_config:ModelTrainerConfig):
        try:

            self.data_transformation_artifacts=data_transformation_artifacts
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model,classificationmetric):
        try:
           
            with mlflow.start_run():
                f1_score=classificationmetric.f1_score
                precision_score=classificationmetric.precision
                recall_score=classificationmetric.recall

                

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision",precision_score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.sklearn.log_model(best_model,"model")
            # #Model registry does not work with file store
            #     if tracking_url_type_store != "file":

            #         # Register the model
            #         # There are other ways to use the Model Registry, which depends on the use case,
            #         # please refer to the doc for more information:
            #         # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            #         mlflow.sklearn.log_model(best_model, "model", registered_model_name=best_model)
            #     else:
            #         mlflow.sklearn.log_model(best_model, "model")

        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def train_model(self,X_train,Y_train,X_test,Y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }
            params={
            "Random Forest": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Decision Tree":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                 'max_features':['sqrt','log2',None],
                #'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }

            
            
            }
            model_report:dict=evaluateModel(X_train,Y_train,X_test,Y_test,models=models,para=params)

            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]


            best_model=models[best_model_name]
            y_train_pred=best_model.predict(X_train)
            
            cr_train=classification_report(Y_train,y_train_pred)

            y_test_pred=best_model.predict(X_test)

            cr_test=classification_report(Y_test,y_test_pred)


            self.track_mlflow(best_model,cr_train)

            preprocessor=load_object(self.data_transformation_artifacts.transformed_object_path)
            
            Network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
            dir_name=os.path.dirname(self.model_trainer_config.model_file_path)
            os.makedirs(dir_name,exist_ok=True)
            save_object(self.model_trainer_config.model_file_path,obj=Network_model)

            save_object('final_model/model.pkl',best_model)

            Model_trainer_artifact=ModelTrainerArtifacts(
                    model_path=self.model_trainer_config.model_file_path,
                    train_model_metrics=cr_train,
                    test_model_metrics=cr_test
                
            )
            return Model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)

   


    def inititate_model_training(self)->ModelTrainerArtifacts:
        try:
            train_path=self.data_transformation_artifacts.transformed_train_path
            test_path=self.data_transformation_artifacts.transformed_test_path

            train_arr=load_numpy_array(train_path)
            test_arr=load_numpy_array(test_path)

            X_train,Y_train,X_test,Y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]

            )
            model_trainer_artifact=self.train_model(X_train,Y_train,X_test,Y_test)

            return model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)     