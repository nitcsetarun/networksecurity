import yaml
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os 
import sys
import dill
import pickle
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml_file(filepath:str) -> dict:
    try:
        with open(filepath,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml_file(folder_path:str,filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(folder_path):
                os.remove(folder_path)
        os.makedirs(folder_path,exist_ok=True)
        with open(filepath,'w')as file:
            yaml.dump(content,file)        
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_to_np(filepath:str,array:np.array)-> None:
    try:
        dirname=os.path.dirname(filepath)
        os.makedirs(dirname,exist_ok=True)
        with open (filepath,'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def save_object(filepath:str,obj:object)-> None:
    try:
        dirname=os.path.dirname(filepath)
        os.makedirs(dirname,exist_ok=True)
        with open (filepath,'wb') as file:
            pickle.dump(obj,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f'File Doesnot Exist{file_path}')
        with open(file_path,'rb')as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)  from e

def load_numpy_array(file_path:str):
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def evaluateModel(X_train,Y_train,X_test,Y_test,models,para):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            params=list(para.values())[i]
            gs=GridSearchCV(model,params,cv=3)

            gs.fit(X_train,Y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=r2_score(Y_train,y_train_pred)
            test_model_score=r2_score(Y_test,y_test_pred)

            report[list(models.keys())[i]]=test_model_score

        return report

            




    except Exception as e:
        raise NetworkSecurityException(e,sys)    
          