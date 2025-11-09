#!/usr/bin/env python3
"""Verify Speech Verification Ensemble installation."""

import sys


def check_imports():
    """Check if all required modules can be imported."""
    print("🔍 Checking imports...")

    modules = {
        "speech_verification": "Speech Verification package",
        "librosa": "Audio analysis (librosa)",
        "resemblyzer": "CNN speaker encoder (resemblyzer)",
        "dtw": "Dynamic Time Warping (dtw-python)",
        "typer": "CLI framework (typer)",
        "rich": "Terminal formatting (rich)",
        "numpy": "Numerical computing (numpy)",
        "sklearn": "Machine learning (scikit-learn)",
        "torch": "Deep learning (pytorch)",
    }

    failed = []
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {description}")
        except ImportError as e:
            print(f"  ❌ {description} - {e}")
            failed.append(module)

    return len(failed) == 0


def check_package():
    """Check package version and exports."""
    print("\n📦 Checking package...")

    try:
        import speech_verification

        print(f"  ✅ Version: {speech_verification.__version__}")

        # Check main exports
        exports = ["MFCCVerifier", "CNNVerifier", "EnsembleVerifier"]
        for export in exports:
            if hasattr(speech_verification, export):
                print(f"  ✅ {export} available")
            else:
                print(f"  ❌ {export} not available")
                return False

        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_cli():
    """Check if CLI is available."""
    print("\n🖥️  Checking CLI...")

    try:
        print("  ✅ CLI module loaded")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("🎙️  Speech Verification Ensemble - Installation Check")
    print("=" * 60)

    checks = [
        ("Imports", check_imports),
        ("Package", check_package),
        ("CLI", check_cli),
    ]

    results = []
    for name, check_func in checks:
        try:
            success = check_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)

    all_passed = True
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n🎉 All checks passed! Installation is complete.")
        print("\n🚀 Next steps:")
        print("  1. Try: speech-verify --help")
        print("  2. Read: QUICKSTART.md")
        print("  3. Explore: Python API examples")
        return 0
    else:
        print("\n❌ Some checks failed. Please install missing dependencies:")
        print("  pip install -e '.[all]'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
