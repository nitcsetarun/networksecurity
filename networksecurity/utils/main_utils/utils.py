import yaml
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os 
import sys
import dill
import pickle


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