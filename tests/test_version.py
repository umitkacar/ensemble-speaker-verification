"""Test version and imports."""

import speech_verification


def test_version():
    """Test that version is defined."""
    assert hasattr(speech_verification, "__version__")
    assert isinstance(speech_verification.__version__, str)
    assert len(speech_verification.__version__) > 0


def test_imports():
    """Test that main classes can be imported."""
    from speech_verification import CNNVerifier, EnsembleVerifier, MFCCVerifier

    assert CNNVerifier is not None
    assert MFCCVerifier is not None
    assert EnsembleVerifier is not None
