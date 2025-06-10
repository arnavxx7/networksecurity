import os
import sys
import numpy as np
import pandas as pd

'''
Defining common constants for training pipeline
'''
TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurity"
FILE_NAME = "phisingData.csv"
ARTIFACTS_DIR = "Artifacts"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

'''
Data Ingestion constants start with DATA_INGESTION
'''

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "Network_Security_DB"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


'''
Data Validation constants start with DATA_VALIDATION
'''

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DATA_DIR: str = "validated"
DATA_VALIDATION_INVALID_DATA_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH: str = "report.yaml"


'''
Data Transformation constants starts with DATA_TRANSFORMATION
'''

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed_data" 
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

#knn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
} 

'''
Model Trainer constants start with MODEL_TRAINER
'''
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05


TRAINING_BUCKET_NAME = "networksecurityprojs3"