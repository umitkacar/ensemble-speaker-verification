#!/usr/bin/env python3
"""Test package without heavy dependencies installed."""

import sys
from pathlib import Path


def test_config_module():
    """Test config module works without dependencies."""
    try:
        from speech_verification.config import Config, AudioConfig, VerificationConfig

        # Create instances
        audio_cfg = AudioConfig()
        verify_cfg = VerificationConfig()
        config = Config()

        # Verify defaults
        assert audio_cfg.sample_rate == 16000
        assert audio_cfg.n_mfcc == 13
        assert verify_cfg.mfcc_threshold == 9000.0
        assert verify_cfg.cnn_threshold == 0.80
        assert verify_cfg.device == "cpu"

        # Test that directories are created
        assert config.data_dir.exists()
        assert config.output_dir.exists()

        print("✅ Config module works without dependencies")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_package_structure():
    """Test package structure is correct."""
    try:
        import speech_verification

        # Check version
        assert hasattr(speech_verification, "__version__")
        assert speech_verification.__version__ == "2.0.0"

        # Check __all__ exports
        expected = ["MFCCVerifier", "CNNVerifier", "EnsembleVerifier", "Config"]
        for export in expected:
            assert export in speech_verification.__all__, f"{export} not in __all__"

        print("✅ Package structure is correct")
        return True
    except Exception as e:
        print(f"❌ Package structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_lazy_imports():
    """Test lazy import mechanism."""
    try:
        import speech_verification

        # These should be accessible via __getattr__ even if dependencies aren't installed
        # But we shouldn't try to actually instantiate them
        assert hasattr(speech_verification, "__getattr__")

        print("✅ Lazy import mechanism exists")
        return True
    except Exception as e:
        print(f"❌ Lazy import test failed: {e}")
        return False


def test_utils_exists():
    """Test that utils modules exist."""
    try:
        from speech_verification import utils

        # Check submodules exist
        assert hasattr(utils, "__file__")

        print("✅ Utils package exists")
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False


def test_core_exists():
    """Test that core modules exist."""
    try:
        from speech_verification import core

        # Check submodules exist
        assert hasattr(core, "__file__")

        print("✅ Core package exists")
        return True
    except Exception as e:
        print(f"❌ Core test failed: {e}")
        return False


def main():
    """Run all tests without dependencies."""
    print("=" * 60)
    print("🧪 Testing Package Without Dependencies")
    print("=" * 60)

    tests = [
        ("Config Module", test_config_module),
        ("Package Structure", test_package_structure),
        ("Lazy Imports", test_lazy_imports),
        ("Utils Package", test_utils_exists),
        ("Core Package", test_core_exists),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Unexpected error in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    print("=" * 60)
    print("📊 Test Results")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
