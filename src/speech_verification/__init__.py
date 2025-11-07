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

from speech_verification.core.mfcc import MFCCVerifier
from speech_verification.core.cnn import CNNVerifier
from speech_verification.core.fusion import EnsembleVerifier

__all__ = [
    "MFCCVerifier",
    "CNNVerifier",
    "EnsembleVerifier",
    "__version__",
]
