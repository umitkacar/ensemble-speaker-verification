"""Utility modules."""

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


def __getattr__(name):
    """Lazy import for better error handling."""
    if name in ["load_audio", "convert_audio", "record_audio"]:
        from speech_verification.utils import audio

        return getattr(audio, name)
    elif name in ["calculate_roc_metrics", "plot_roc_curve"]:
        from speech_verification.utils import metrics

        return getattr(metrics, name)
    elif name in ["plot_waveform", "plot_mfcc_comparison", "plot_confusion_matrix"]:
        from speech_verification.utils import visualization

        return getattr(visualization, name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
