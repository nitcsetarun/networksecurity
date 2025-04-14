from networksecurity.exceptions.exception import NetworkSecurityException
from sklearn.metrics import recall_score,precision_score,f1_score

from networksecurity.entity.data_artifacts import ClassificationMetricsArtifacts

def classification_report(y_true,y_pred)->ClassificationMetricsArtifacts:
    f1=f1_score(y_true,y_pred)
    precision=precision_score(y_true,y_pred)
    recall=recall_score(y_true,y_pred)

    ClassificationReport=ClassificationMetricsArtifacts(
        f1_score=f1,
        precision=precision,
        recall=recall
    )

    return ClassificationReport