"""Visualization utilities."""

import logging
from pathlib import Path
from typing import Optional, Union

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

logger = logging.getLogger(__name__)


def plot_waveform(
    y: np.ndarray,
    sr: int,
    title: str = "Waveform",
    save_path: Optional[Union[str, Path]] = None,
) -> None:
    """
    Plot audio waveform.

    Args:
        y: Audio array
        sr: Sample rate
        title: Plot title
        save_path: Path to save plot (optional)
    """
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=sr, alpha=0.8)
    plt.title(title, fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"Waveform plot saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_mfcc_comparison(
    mfcc1: np.ndarray,
    mfcc2: np.ndarray,
    sr: int = 16000,
    title1: str = "MFCC 1",
    title2: str = "MFCC 2",
    save_path: Optional[Union[str, Path]] = None,
) -> None:
    """
    Plot comparison of two MFCC feature matrices.

    Args:
        mfcc1: First MFCC matrix
        mfcc2: Second MFCC matrix
        sr: Sample rate
        title1: Title for first MFCC
        title2: Title for second MFCC
        save_path: Path to save plot (optional)
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot first MFCC
    img1 = librosa.display.specshow(
        mfcc1,
        sr=sr,
        x_axis="time",
        ax=axes[0],
        cmap="viridis",
    )
    axes[0].set_title(title1, fontsize=14)
    axes[0].set_ylabel("MFCC Coefficients", fontsize=12)
    fig.colorbar(img1, ax=axes[0], format="%+2.0f dB")

    # Plot second MFCC
    img2 = librosa.display.specshow(
        mfcc2,
        sr=sr,
        x_axis="time",
        ax=axes[1],
        cmap="viridis",
    )
    axes[1].set_title(title2, fontsize=14)
    axes[1].set_ylabel("MFCC Coefficients", fontsize=12)
    fig.colorbar(img2, ax=axes[1], format="%+2.0f dB")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"MFCC comparison saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_confusion_matrix(
    cm: np.ndarray,
    labels: Optional[list[str]] = None,
    title: str = "Confusion Matrix",
    save_path: Optional[Union[str, Path]] = None,
    normalize: bool = False,
) -> None:
    """
    Plot confusion matrix.

    Args:
        cm: Confusion matrix
        labels: Class labels
        title: Plot title
        save_path: Path to save plot (optional)
        normalize: Normalize values to percentages
    """
    if labels is None:
        labels = ["Different", "Same"]

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        fmt = ".2%"
    else:
        fmt = "d"

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt=fmt,
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar_kws={"label": "Count" if not normalize else "Percentage"},
    )
    plt.title(title, fontsize=14)
    plt.ylabel("True Label", fontsize=12)
    plt.xlabel("Predicted Label", fontsize=12)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"Confusion matrix saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_spectrogram(
    y: np.ndarray,
    sr: int,
    title: str = "Spectrogram",
    save_path: Optional[Union[str, Path]] = None,
) -> None:
    """
    Plot audio spectrogram.

    Args:
        y: Audio array
        sr: Sample rate
        title: Plot title
        save_path: Path to save plot (optional)
    """
    plt.figure(figsize=(14, 6))

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="hz", cmap="magma")

    plt.colorbar(img, format="%+2.0f dB")
    plt.title(title, fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Frequency (Hz)", fontsize=12)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"Spectrogram saved to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_multi_roc(
    roc_curves: dict[str, dict],
    title: str = "ROC Curves Comparison",
    save_path: Optional[Union[str, Path]] = None,
) -> None:
    """
    Plot multiple ROC curves on same figure.

    Args:
        roc_curves: Dict of {method_name: roc_metrics}
        title: Plot title
        save_path: Path to save plot (optional)
    """
    plt.figure(figsize=(10, 8))

    colors = ["darkorange", "green", "red", "purple", "brown"]

    for i, (name, metrics) in enumerate(roc_curves.items()):
        color = colors[i % len(colors)]
        plt.plot(
            metrics["fpr"],
            metrics["tpr"],
            color=color,
            lw=2,
            label=f'{name} (AUC = {metrics["auc"]:.4f})',
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
        logger.info(f"Multi-ROC plot saved to {save_path}")
    else:
        plt.show()

    plt.close()
