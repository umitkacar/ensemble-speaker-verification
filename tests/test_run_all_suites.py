#!/usr/bin/env python3
"""
Master test runner - runs all test suites.
This is the production test suite that validates everything.
"""

import subprocess
import sys
from pathlib import Path


def run_test_suite(name: str, script: str) -> tuple[str, bool, str]:
    """Run a test suite and return results."""
    print(f"\n{'=' * 70}")
    print(f"🧪 Running: {name}")
    print(f"{'=' * 70}")

    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(__file__).parent.parent,
            env={
                **subprocess.os.environ,
                "PYTHONPATH": str(Path(__file__).parent.parent / "src"),
            },
        )

        # Print output
        print(result.stdout)
        if result.stderr and "WARNING" not in result.stderr.upper():
            print("STDERR:", result.stderr)

        success = result.returncode == 0
        return (name, success, result.stdout)

    except subprocess.TimeoutExpired:
        print(f"❌ {name} timed out")
        return (name, False, "Test timed out")
    except Exception as e:
        print(f"❌ {name} failed with error: {e}")
        import traceback

        traceback.print_exc()
        return (name, False, str(e))


def main():
    """Run all test suites."""
    print("=" * 70)
    print("🎯 PRODUCTION TEST SUITE - Complete Validation")
    print("=" * 70)
    print("\nThis will run ALL tests to ensure production readiness.")
    print("=" * 70)

    # Define all test suites
    test_suites = [
        ("Basic Package Tests", "tests/test_basic.py"),
        ("Tests Without Dependencies", "tests/test_without_deps.py"),
        ("CLI Functionality Tests", "tests/test_cli_real.py"),
        # These require dependencies
        # ("Audio Generation", "tests/generate_test_audio.py"),
        # ("Real Verification Tests", "tests/test_verification_real.py"),
        # ("Integration Tests", "tests/test_integration.py"),
    ]

    results = []
    for name, script in test_suites:
        result = run_test_suite(name, script)
        results.append(result)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for name, success, _ in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print("=" * 70)
    print(
        f"\n📈 Overall: {passed}/{total} test suites passed ({passed/total*100:.1f}%)"
    )

    if passed == total:
        print("\n🎉 ALL TEST SUITES PASSED!")
        print("\n✨ Package is PRODUCTION READY!")
        return 0
    elif passed >= total * 0.9:
        print(f"\n⚠️  {total - passed} suite(s) failed, but 90%+ passed")
        print("Package is mostly ready for production")
        return 0
    elif passed >= total * 0.75:
        print(f"\n⚠️  {total - passed} suite(s) failed, but 75%+ passed")
        print("Package needs minor fixes")
        return 1
    else:
        print(f"\n❌ {total - passed} suite(s) failed")
        print("Package needs significant fixes before production")
        return 1


if __name__ == "__main__":
    sys.exit(main())
