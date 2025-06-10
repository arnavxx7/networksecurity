import os, sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, 
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_target_input(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        target_feature_df = dataframe[TARGET_COLUMN]
        input_feature_df = dataframe.drop(columns=TARGET_COLUMN)
        target_feature_df = target_feature_df.replace(-1,0)
        return input_feature_df, target_feature_df
    
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Initialises KNN imputer object with parameters defined in constants->training_pipeline,
        Returns pipeline object with the first step as KNN Imputer 
        """
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Initialise KNN object")
            preprocessor: Pipeline = Pipeline([("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path
            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)
            X_train, y_train = self.split_target_input(train_df)
            X_test, y_test = self.split_target_input(test_df)

            # get the preprocessor pipeline
            preprocessor = self.get_data_transformer_object()

            # fit the pipeline with training data
            preprocessor_obj = preprocessor.fit(X_train)

            # get the transformed array for training and test data
            transformed_X_train = preprocessor_obj.transform(X_train)
            transformed_X_test = preprocessor_obj.transform(X_test)

            # combine the transformed input features array with target features
            train_arr = np.c_[transformed_X_train, np.array(y_train)]
            test_arr = np.c_[transformed_X_test, np.array(y_test)]

            # save numpy arrays and preprocessing object
            save_numpy_array(file_path=self.data_transformation_config.transformed_trained_file_path, array=train_arr)
            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_obj)

            # saving preprocessing pipeline to final_model
            save_object(file_path="final_model/preprocessor.pkl", obj=preprocessor_obj)

            # preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_trained_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)