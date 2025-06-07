import os, sys
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np

def get_classification_metrics(actual: np.array, pred: np.array)-> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true=actual, y_pred=pred)
        model_precision_score = precision_score(y_true=actual, y_pred=pred)
        model_recall_score = recall_score(y_true=actual, y_pred=pred)

        classification_metric_artifact = ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )

        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)