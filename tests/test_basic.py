"""Test core functionality without heavy dependencies."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_package_import():
    """Test that package can be imported."""
    import speech_verification

    assert speech_verification.__version__ == "2.0.0"
    assert "MFCCVerifier" in speech_verification.__all__
    assert "CNNVerifier" in speech_verification.__all__
    assert "EnsembleVerifier" in speech_verification.__all__
    print("✅ Package import test passed")


def test_lazy_imports():
    """Test lazy import mechanism."""
    import speech_verification

    # These should not fail even without dependencies
    # because of lazy loading
    assert hasattr(speech_verification, "__getattr__")
    print("✅ Lazy import mechanism test passed")


def test_version():
    """Test version is accessible."""
    from speech_verification import __version__

    assert isinstance(__version__, str)
    assert len(__version__) > 0
    print(f"✅ Version test passed: {__version__}")


def test_config_import():
    """Test config module."""
    try:
        from speech_verification.config import Config, AudioConfig, VerificationConfig

        config = Config()
        assert config.audio.sample_rate == 16000
        assert config.verification.device in ["cpu", "cuda"]
        print("✅ Config module test passed")
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        raise


def test_package_structure():
    """Test package structure."""
    import speech_verification

    # Check __all__ is defined
    assert hasattr(speech_verification, "__all__")
    assert len(speech_verification.__all__) > 0

    # Check version attributes
    assert hasattr(speech_verification, "__version__")
    assert hasattr(speech_verification, "__author__")
    assert hasattr(speech_verification, "__license__")

    print("✅ Package structure test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Running Production Tests")
    print("=" * 60)

    tests = [
        test_package_import,
        test_lazy_imports,
        test_version,
        test_config_import,
        test_package_structure,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            failed.append((test.__name__, str(e)))
            print(f"❌ {test.__name__} FAILED: {e}")

    print("=" * 60)
    if not failed:
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"❌ {len(failed)} TESTS FAILED:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("=" * 60)
        sys.exit(1)
