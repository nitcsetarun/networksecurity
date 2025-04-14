from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

from networksecurity.exceptions.exception import NetworkSecurityException

import os
import sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.predict(x_transform)

            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)    