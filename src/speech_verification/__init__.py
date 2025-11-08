"""
Speech Verification Ensemble - A multi-modal speaker verification system.

This package provides state-of-the-art speaker verification using:
- MFCC + DTW (Dynamic Time Warping)
- Resemblyzer CNN (Deep Learning)
- Score-Level Fusion

Copyright (c) 2024-2025 Speech-Verification-Ensemble Contributors
Licensed under MIT License
"""

__version__ = "2.0.0"
__author__ = "Speech Verification Ensemble Contributors"
__license__ = "MIT"

# Lazy imports for better error handling
__all__ = [
    "MFCCVerifier",
    "CNNVerifier",
    "EnsembleVerifier",
    "Config",
    "__version__",
]


def __getattr__(name):
    """Lazy import for better error handling."""
    if name == "MFCCVerifier":
        from speech_verification.core.mfcc import MFCCVerifier

        return MFCCVerifier
    elif name == "CNNVerifier":
        from speech_verification.core.cnn import CNNVerifier

        return CNNVerifier
    elif name == "EnsembleVerifier":
        from speech_verification.core.fusion import EnsembleVerifier

        return EnsembleVerifier
    elif name == "Config":
        from speech_verification.config import Config

        return Config
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
