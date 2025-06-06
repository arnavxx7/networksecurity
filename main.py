from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        logging.info("Initiate data ingestion")
        data_ingestion = DataIngestion(data_ingestion_config)
        ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(ingestion_artifact.training_file_path)
        print(ingestion_artifact.testing_file_path)
        logging.info("Data Ingestion Completed")
        logging.info("Initiate Data Validation")
        data_validation = DataValidation(ingestion_artifact, data_validation_config)
        validation_artifact = data_validation.initiate_data_validation()
        if validation_artifact.validation_status:
            print("Data drift has not ocurred")
        else:
            print("Data drift has ocurred")
        print(validation_artifact.drift_report_file_path)
        logging.info("Data Validation Completed")
        logging.info("Initiate Data Transformation")
        data_transformation = DataTransformation(validation_artifact, data_transformation_config)
        transformation_artifact = data_transformation.initiate_data_transformation()
        print(transformation_artifact.transformed_train_file_path)
        print(transformation_artifact.transformed_object_file_path)
        logging.info("Data Transformation Completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)