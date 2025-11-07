"""Metrics and evaluation utilities."""

import logging
from typing import Optional

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

logger = logging.getLogger(__name__)


def calculate_roc_metrics(
    predictions: np.ndarray, labels: np.ndarray
) -> dict:
    """
    Calculate ROC curve metrics.

    Args:
        predictions: Predicted distances/scores
        labels: Ground truth labels (1=same speaker, 0=different)

    Returns:
        Dictionary with TPR, FPR, thresholds, and AUC
    """
    fpr, tpr, thresholds = roc_curve(labels, predictions)
    roc_auc = roc_auc_score(labels, predictions)

    logger.info(f"ROC AUC Score: {roc_auc:.4f}")

    return {
        "fpr": fpr,
        "tpr": tpr,
        "thresholds": thresholds,
        "auc": roc_auc,
    }


def calculate_pr_metrics(
    predictions: np.ndarray, labels: np.ndarray
) -> dict:
    """
    Calculate Precision-Recall curve metrics.

    Args:
        predictions: Predicted distances/scores
        labels: Ground truth labels

    Returns:
        Dictionary with precision, recall, thresholds, and AUC
    """
    precision, recall, thresholds = precision_recall_curve(labels, predictions)
    pr_auc = auc(recall, precision)

    logger.info(f"PR AUC Score: {pr_auc:.4f}")

    return {
        "precision": precision,
        "recall": recall,
        "thresholds": thresholds,
        "auc": pr_auc,
    }


def calculate_eer(
    predictions: np.ndarray, labels: np.ndarray
) -> tuple[float, float]:
    """
    Calculate Equal Error Rate (EER).

    Args:
        predictions: Predicted distances/scores
        labels: Ground truth labels

    Returns:
        Tuple of (eer, threshold)
    """
    fpr, tpr, thresholds = roc_curve(labels, predictions)
    fnr = 1 - tpr

    # Find where FPR and FNR are equal
    eer_threshold = thresholds[np.nanargmin(np.absolute((fnr - fpr)))]
    eer = fpr[np.nanargmin(np.absolute((fnr - fpr)))]

    logger.info(f"EER: {eer:.4f} at threshold {eer_threshold:.4f}")

    return float(eer), float(eer_threshold)


def calculate_classification_metrics(
    y_true: np.ndarray, y_pred: np.ndarray
) -> dict:
    """
    Calculate classification metrics.

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels

    Returns:
        Dictionary with accuracy, precision, recall, and F1-score
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
    }

    logger.info(
        f"Accuracy: {metrics['accuracy']:.4f}, "
        f"Precision: {metrics['precision']:.4f}, "
        f"Recall: {metrics['recall']:.4f}, "
        f"F1: {metrics['f1']:.4f}"
    )

    return metrics


def plot_roc_curve(
    roc_metrics: dict,
    title: str = "ROC Curve",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot ROC curve.

    Args:
        roc_metrics: Dictionary from calculate_roc_metrics()
        title: Plot title
        save_path: Path to save plot (optional)
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.error("matplotlib not installed")
        return

    plt.figure(figsize=(10, 8))
    plt.plot(
        roc_metrics["fpr"],
        roc_metrics["tpr"],
        color="darkorange",
        lw=2,
        label=f'ROC curve (AUC = {roc_metrics["auc"]:.4f})',
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Random")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate", fontsize=12)
    plt.ylabel("True Positive Rate", fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"ROC curve saved to {save_path}")
    else:
        plt.show()

    plt.close()


def calculate_optimal_threshold(
    predictions: np.ndarray,
    labels: np.ndarray,
    metric: str = "f1",
) -> tuple[float, float]:
    """
    Find optimal threshold based on specified metric.

    Args:
        predictions: Predicted distances/scores
        labels: Ground truth labels
        metric: Metric to optimize ('f1', 'accuracy', 'balanced')

    Returns:
        Tuple of (optimal_threshold, metric_value)
    """
    if metric == "eer":
        eer, threshold = calculate_eer(predictions, labels)
        return threshold, eer

    # Try different thresholds
    thresholds = np.linspace(predictions.min(), predictions.max(), 1000)
    best_metric = 0.0
    best_threshold = 0.0

    for threshold in thresholds:
        y_pred = (predictions >= threshold).astype(int)

        if metric == "f1":
            score = f1_score(labels, y_pred, zero_division=0)
        elif metric == "accuracy":
            score = accuracy_score(labels, y_pred)
        elif metric == "balanced":
            prec = precision_score(labels, y_pred, zero_division=0)
            rec = recall_score(labels, y_pred, zero_division=0)
            score = 2 * (prec * rec) / (prec + rec + 1e-10)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        if score > best_metric:
            best_metric = score
            best_threshold = threshold

    logger.info(
        f"Optimal threshold: {best_threshold:.4f} "
        f"({metric}={best_metric:.4f})"
    )

    return float(best_threshold), float(best_metric)
