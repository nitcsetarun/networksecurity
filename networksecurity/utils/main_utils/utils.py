import yaml
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os 
import sys
import dill
import pickle
import numpy as np


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