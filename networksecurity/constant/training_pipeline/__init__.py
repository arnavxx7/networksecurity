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

'''
Data Ingestion constants start with DATA_INGESTION
'''

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "Network_Security_DB"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2