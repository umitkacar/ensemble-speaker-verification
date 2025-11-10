#!/usr/bin/env python3
"""
Generate test audio files for verification testing.
Creates simple audio samples that can be used to test the verification pipeline.
"""

import sys
from pathlib import Path


def generate_test_audio():
    """Generate test audio files using numpy."""
    try:
        import numpy as np
        import soundfile as sf

        print("🎵 Generating test audio files...")

        # Create output directory
        output_dir = Path("./data/test_audio")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Audio parameters
        sample_rate = 16000
        duration = 3  # seconds

        # Generate 3 different "speakers" with different frequencies
        speakers = {
            "speaker1": 220,  # A3
            "speaker2": 440,  # A4
            "speaker3": 880,  # A5
        }

        for speaker_name, frequency in speakers.items():
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = np.sin(2 * np.pi * frequency * t)

            # Add some variation to make it more realistic
            envelope = np.exp(-t / duration * 2)  # Decay envelope
            audio = audio * envelope

            # Normalize
            audio = audio / np.max(np.abs(audio)) * 0.8

            # Save as WAV file
            output_file = output_dir / f"{speaker_name}.wav"
            sf.write(output_file, audio.astype(np.float32), sample_rate)

            print(f"✅ Created: {output_file}")

        # Create enrollment and test files (same speakers)
        for speaker_name in speakers:
            # Enrollment file (copy)
            src = output_dir / f"{speaker_name}.wav"
            dst_enroll = output_dir / f"{speaker_name}_enroll.wav"
            dst_test = output_dir / f"{speaker_name}_test.wav"

            import shutil

            shutil.copy(src, dst_enroll)
            shutil.copy(src, dst_test)

            print(f"✅ Created enrollment/test pair for {speaker_name}")

        print(f"\n✅ Test audio files created in {output_dir}")
        return True

    except ImportError as e:
        print(f"⚠️  Cannot generate audio files: {e}")
        print("This requires numpy and soundfile to be installed.")
        return False
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_audio_files():
    """Verify that audio files were created correctly."""
    output_dir = Path("./data/test_audio")

    if not output_dir.exists():
        print("❌ Test audio directory doesn't exist")
        return False

    expected_files = [
        "speaker1.wav",
        "speaker2.wav",
        "speaker3.wav",
        "speaker1_enroll.wav",
        "speaker1_test.wav",
        "speaker2_enroll.wav",
        "speaker2_test.wav",
        "speaker3_enroll.wav",
        "speaker3_test.wav",
    ]

    all_exist = True
    for filename in expected_files:
        filepath = output_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename} ({size} bytes)")
        else:
            print(f"❌ Missing: {filename}")
            all_exist = False

    return all_exist


def main():
    """Generate and verify test audio files."""
    print("=" * 60)
    print("🎵 Test Audio Generation")
    print("=" * 60)

    # Generate audio files
    if generate_test_audio():
        print("\n" + "=" * 60)
        print("📊 Verifying Generated Files")
        print("=" * 60)

        if verify_audio_files():
            print("\n✅ All test audio files generated successfully!")
            return 0
        else:
            print("\n⚠️  Some audio files are missing")
            return 1
    else:
        print("\n⚠️  Audio generation skipped (dependencies not installed)")
        return 0  # Non-critical


if __name__ == "__main__":
    sys.exit(main())
