from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pandas as pd
import yaml
import pickle
import dill
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path: str, content, replace: bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array(file_path: str, array: np.array):
    '''
    Save numpy array as .npy file
    file_path: Location to save the numpy arrayy
    array: np array to save
    '''
    try:
        logging.info("ENTERED SAVE NUMPY ARRAY METHOD IN UTILS FILE")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info("EXITED SAVE NUMPY ARRAY METHOD IN UTILS FILE")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_object(file_path: str, obj: object):
    '''
    Saves model or pipelines as pkl file.
    file_path: Location of where to save the object
    obj: Model or pipeline to save
    '''
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def load_object(file_path: str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def load_numpy_array(file_path: str)-> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
         raise NetworkSecurityException(e, sys)
    

def evaluate_model(x_train ,y_train, x_test, y_test, models, params)-> dict:
    try:
        report = {}
        best_params = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            model_name = list(models.keys())[i]
            param = params[model_name]
            gs = GridSearchCV(estimator=model, param_grid=param, cv=3)
            gs.fit(x_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            
            train_model_score = r2_score(y_true=y_train, y_pred=y_train_pred)
            test_model_score = r2_score(y_true=y_test, y_pred=y_test_pred)

            report[model_name] = test_model_score
            best_params[model_name] = gs.best_params_
            return report, best_params
    except Exception as e:
        raise NetworkSecurityException(e, sys)