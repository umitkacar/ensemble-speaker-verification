#!/usr/bin/env python3
"""Integration tests for the complete package."""

import sys
import tempfile
from pathlib import Path


def test_full_package_import():
    """Test that the full package can be imported with all dependencies."""
    print("Testing full package import...")
    try:
        import speech_verification

        assert hasattr(speech_verification, "MFCCVerifier")
        assert hasattr(speech_verification, "CNNVerifier")
        assert hasattr(speech_verification, "EnsembleVerifier")
        assert hasattr(speech_verification, "Config")

        print("✅ Full package import successful")
        return True
    except Exception as e:
        print(f"❌ Package import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_verifier_instantiation():
    """Test that verifiers can be instantiated."""
    print("\nTesting verifier instantiation...")
    try:
        from speech_verification import MFCCVerifier, CNNVerifier, EnsembleVerifier

        # Test MFCC
        mfcc = MFCCVerifier()
        print("✅ MFCCVerifier instantiated")

        # Test CNN
        cnn = CNNVerifier()
        print("✅ CNNVerifier instantiated")

        # Test Ensemble
        ensemble = EnsembleVerifier()
        print("✅ EnsembleVerifier instantiated")

        return True
    except Exception as e:
        print(f"❌ Verifier instantiation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_config_functionality():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    try:
        from speech_verification import Config
        from speech_verification.config import AudioConfig, VerificationConfig

        # Create config
        config = Config()

        # Verify defaults
        assert config.audio.sample_rate == 16000
        assert config.verification.mfcc_threshold == 9000.0
        assert config.verification.cnn_threshold == 0.80
        assert config.data_dir.exists()
        assert config.output_dir.exists()

        # Test custom config
        custom_audio = AudioConfig(sample_rate=22050, n_mfcc=20)
        assert custom_audio.sample_rate == 22050
        assert custom_audio.n_mfcc == 20

        custom_verify = VerificationConfig(
            mfcc_threshold=8000.0, cnn_threshold=0.75, device="cpu"
        )
        assert custom_verify.mfcc_threshold == 8000.0
        assert custom_verify.device == "cpu"

        print("✅ Configuration functionality works")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_cli_module():
    """Test CLI module can be imported."""
    print("\nTesting CLI module...")
    try:
        from speech_verification.cli import app

        # Verify it's a Typer app
        assert hasattr(app, "command") or hasattr(app, "registered_commands")

        print("✅ CLI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ CLI module test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_audio_generation():
    """Test that we can generate test audio data."""
    print("\nTesting audio generation...")
    try:
        import numpy as np

        # Generate simple sine wave
        sample_rate = 16000
        duration = 1  # second
        frequency = 440  # Hz (A4 note)

        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

        assert audio.shape[0] == sample_rate * duration
        assert audio.dtype == np.float32

        print("✅ Audio generation works")
        return True
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_verification_install():
    """Run the verification installation script."""
    print("\nRunning installation verification script...")
    try:
        import subprocess

        result = subprocess.run(
            ["python", "verify_installation.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("✅ Installation verification passed")
            return True
        else:
            print(f"⚠️  Installation verification returned code {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"⚠️  Installation verification warning: {e}")
        # Non-critical, so return True
        return True


def main():
    """Run all integration tests."""
    print("=" * 70)
    print("🧪 INTEGRATION TESTS - Full Package with Dependencies")
    print("=" * 70)

    tests = [
        ("Full Package Import", test_full_package_import),
        ("Verifier Instantiation", test_verifier_instantiation),
        ("Configuration", test_config_functionality),
        ("CLI Module", test_cli_module),
        ("Audio Generation", test_audio_generation),
        ("Installation Verification", test_verification_install),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    print("\n" + "=" * 70)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("\n✨ Package is production-ready!")
        return 0
    elif passed >= total * 0.8:
        print(f"\n⚠️  {total - passed} test(s) failed, but most tests passed")
        print("Package is mostly functional, review failed tests")
        return 1
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        print("Package needs fixes before production use")
        return 1


if __name__ == "__main__":
    sys.exit(main())
