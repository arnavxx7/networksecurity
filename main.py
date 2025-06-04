from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__=="__main__":
    try:
        logging.info("Executing data ingestion")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        artifact_obj = data_ingestion.initiate_data_ingestion()
        print(artifact_obj.training_file_path)
        print(artifact_obj.testing_file_path)
    except Exception as e:
        raise NetworkSecurityException(e, sys)