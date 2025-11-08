"""Core verification modules."""

__all__ = ["MFCCVerifier", "CNNVerifier", "EnsembleVerifier"]


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
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
