"""Utility modules."""

from speech_verification.utils.audio import convert_audio, load_audio, record_audio
from speech_verification.utils.metrics import calculate_roc_metrics, plot_roc_curve
from speech_verification.utils.visualization import (
    plot_confusion_matrix,
    plot_mfcc_comparison,
    plot_waveform,
)

__all__ = [
    "load_audio",
    "convert_audio",
    "record_audio",
    "calculate_roc_metrics",
    "plot_roc_curve",
    "plot_waveform",
    "plot_mfcc_comparison",
    "plot_confusion_matrix",
]
