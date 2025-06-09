import os, sys

import mlflow.sklearn
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import load_numpy_array, load_object, save_object, evaluate_model
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metrics
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact, ModelTrainerArtifact, DataTransformationArtifact

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
import mlflow




class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, best_model, classification_metrics):
        try:
            with mlflow.start_run():
                f1_score = classification_metrics.f1_score
                precision_score = classification_metrics.precision_score
                recall_score = classification_metrics.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall score", recall_score)
                mlflow.sklearn.log_model(sk_model=best_model, artifact_path="model")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1,),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(),
                "AdaBoost": AdaBoostClassifier()
            }
            params = {
                "Random Forest": {"n_estimators": [100, 150, 200, 300]},
                "Decision Tree": {"criterion": ['gini', 'entropy', 'log_loss']},
                "Gradient Boosting": {"loss": ['log_loss', 'deviance', 'exponential']},
                "Logistic Regression": {"penalty": ['l1', 'l2', 'elasticnet']},
                "AdaBoost": {"learning_rate": [0.8, 1.0, 1.2, 2.0]}
            }

            model_report, param_report = evaluate_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, params=params)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            best_model.set_params(**param_report[best_model_name])
            best_model.fit(x_train, y_train)
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)
            train_metrics = get_classification_metrics(actual=y_train, pred=y_train_pred)
            test_metrics = get_classification_metrics(actual=y_test, pred=y_test_pred)
            #Track the experiments with ml flow
            self.track_mlflow(best_model, train_metrics)
            self.track_mlflow(best_model, test_metrics)
            # Load preprocessor pipeline to give to network model class
            preprocessor_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)
            # make directory for saving model
            model_dir = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor_obj, model=best_model)
            
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

            # Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact = train_metrics,
                test_metric_artifact=test_metrics
            )
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)