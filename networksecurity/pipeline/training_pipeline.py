import os, sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME

from networksecurity.entity.config_entity import *
from networksecurity.entity.artifact_entity import *



class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            self.s3_sync = S3Sync()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info("Starting Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed with artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self):
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            logging.info("Start Data Validation")
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed with artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self):
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_validation_artifact: DataValidationArtifact = self.start_data_validation()
            logging.info("Start Data Transformation")
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation completed with artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_trainer(self):
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation()
            logging.info("Start Model Training")
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training completed with artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    # sync local artifacts folder to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_uri = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_S3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_uri)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    # sync local final model folder to s3 bucket
    def sync_model_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_S3(folder=self.training_pipeline_config.model_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            model_trainer_artifact = self.start_model_trainer()
            self.sync_artifact_dir_to_s3()
            self.sync_model_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)