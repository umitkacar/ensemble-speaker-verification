# Quick Start Guide 🚀

Get started with Speech Verification Ensemble in 5 minutes!

## Installation

### Option 1: Install from PyPI (when published)

```bash
pip install speech-verification-ensemble
```

### Option 2: Install from source

```bash
# Clone the repository
git clone https://github.com/umitkacar/Speech-Verification-Ensemble.git
cd Speech-Verification-Ensemble

# Install in development mode
pip install -e .

# Or install with all optional dependencies
pip install -e ".[all]"
```

## Basic Usage

### 1. Command Line Interface (CLI)

#### Verify Two Audio Files

```bash
# Using ensemble method (recommended)
speech-verify verify speaker1.wav speaker2.wav

# Using only MFCC
speech-verify verify audio1.wav audio2.wav --method mfcc

# Using CNN with verbose output
speech-verify verify audio1.wav audio2.wav --method cnn --verbose

# Output as JSON
speech-verify verify audio1.wav audio2.wav --json
```

#### Record Audio

```bash
# Record 5 seconds (default)
speech-verify record my_voice.wav

# Record 10 seconds
speech-verify record my_voice.wav --duration 10
```

#### Convert Audio Format

```bash
# Convert MP3 to WAV
speech-verify convert input.mp3 output.wav

# Convert with specific sample rate
speech-verify convert input.mp3 output.wav --sr 16000
```

#### Batch Processing

```bash
# Create a pairs file (pairs.json)
echo '[
  ["speaker1_sample1.wav", "speaker1_sample2.wav"],
  ["speaker2_sample1.wav", "speaker2_sample2.wav"]
]' > pairs.json

# Run batch verification
speech-verify batch pairs.json --output results.json
```

### 2. Python API

#### Simple Verification

```python
from speech_verification import EnsembleVerifier

# Initialize verifier
verifier = EnsembleVerifier()

# Verify two audio files
is_same_speaker = verifier.verify("audio1.wav", "audio2.wav")

if is_same_speaker:
    print("✅ Same speaker!")
else:
    print("❌ Different speakers")
```

#### Detailed Results

```python
from speech_verification import EnsembleVerifier

verifier = EnsembleVerifier()

# Get detailed results
result = verifier.verify("audio1.wav", "audio2.wav", return_details=True)

print(f"Same speaker: {result['is_same_speaker']}")
print(f"Fusion score: {result['fusion_score']:.4f}")
print(f"MFCC result: {result['mfcc']['result']}")
print(f"CNN result: {result['cnn']['result']}")
```

#### Using Individual Verifiers

```python
from speech_verification import MFCCVerifier, CNNVerifier

# MFCC + DTW
mfcc_verifier = MFCCVerifier()
is_same, distance = mfcc_verifier.verify(
    "audio1.wav", "audio2.wav", return_distance=True
)
print(f"MFCC distance: {distance:.2f}")

# CNN (Resemblyzer)
cnn_verifier = CNNVerifier()
is_same, distance = cnn_verifier.verify(
    "audio1.wav", "audio2.wav", return_distance=True
)
print(f"CNN distance: {distance:.4f}")
```

#### Batch Processing

```python
from speech_verification import EnsembleVerifier

verifier = EnsembleVerifier()

# Prepare audio pairs
pairs = [
    ("speaker1_a.wav", "speaker1_b.wav"),
    ("speaker2_a.wav", "speaker2_b.wav"),
    ("speaker1_a.wav", "speaker2_a.wav"),
]

# Batch verify
results = verifier.batch_verify(pairs)

for i, result in enumerate(results):
    print(f"Pair {i+1}: {result['is_same_speaker']}")
```

#### Custom Configuration

```python
from speech_verification import EnsembleVerifier
from speech_verification.config import Config, VerificationConfig

# Create custom config
config = Config()
config.verification.mfcc_threshold = 8000.0  # More strict
config.verification.cnn_threshold = 0.75     # More strict
config.verification.device = "cuda"          # Use GPU

# Initialize with custom config
verifier = EnsembleVerifier(verification_config=config.verification)
```

#### Audio Utilities

```python
from speech_verification.utils.audio import (
    load_audio,
    convert_audio,
    normalize_audio,
    trim_silence
)

# Load audio
audio, sr = load_audio("input.wav", sr=16000)

# Normalize
audio_normalized = normalize_audio(audio)

# Trim silence
audio_trimmed, (start, end) = trim_silence(audio, sr)

# Convert format
convert_audio("input.mp3", "output.wav", sr=16000)
```

#### Visualization

```python
from speech_verification.utils.visualization import (
    plot_waveform,
    plot_mfcc_comparison,
    plot_spectrogram
)
from speech_verification.utils.audio import load_audio
from speech_verification.core.mfcc import MFCCVerifier

# Load audio
audio, sr = load_audio("audio.wav")

# Plot waveform
plot_waveform(audio, sr, title="My Audio", save_path="waveform.png")

# Plot spectrogram
plot_spectrogram(audio, sr, title="Spectrogram", save_path="spec.png")

# Compare MFCCs
verifier = MFCCVerifier()
mfcc1 = verifier.extract_mfcc("audio1.wav")
mfcc2 = verifier.extract_mfcc("audio2.wav")
plot_mfcc_comparison(mfcc1, mfcc2, save_path="mfcc_compare.png")
```

## Examples

### Example 1: Identity Verification System

```python
from speech_verification import EnsembleVerifier
from pathlib import Path

class VoiceAuth:
    def __init__(self, enrollment_dir: str):
        self.verifier = EnsembleVerifier()
        self.enrollment_dir = Path(enrollment_dir)

    def enroll_user(self, user_id: str, voice_sample: str):
        """Enroll a user with their voice sample."""
        target = self.enrollment_dir / f"{user_id}.wav"
        target.parent.mkdir(parents=True, exist_ok=True)
        # Copy or convert audio to enrollment directory
        from shutil import copy
        copy(voice_sample, target)
        print(f"✅ User {user_id} enrolled")

    def verify_user(self, user_id: str, voice_sample: str) -> bool:
        """Verify user identity."""
        enrolled = self.enrollment_dir / f"{user_id}.wav"

        if not enrolled.exists():
            print(f"❌ User {user_id} not enrolled")
            return False

        result = self.verifier.verify(enrolled, voice_sample)
        return result

# Usage
auth = VoiceAuth("./enrollments")
auth.enroll_user("john_doe", "john_voice.wav")

# Later, verify
if auth.verify_user("john_doe", "test_voice.wav"):
    print("✅ Access granted")
else:
    print("❌ Access denied")
```

### Example 2: Speaker Identification

```python
from speech_verification import CNNVerifier
from pathlib import Path

def identify_speaker(test_audio: str, reference_dir: str, threshold: float = 0.75):
    """
    Identify which speaker the test audio belongs to.

    Args:
        test_audio: Path to test audio
        reference_dir: Directory with reference audios
        threshold: Maximum distance threshold

    Returns:
        Tuple of (speaker_id, confidence)
    """
    verifier = CNNVerifier()
    reference_files = Path(reference_dir).glob("*.wav")

    best_match = None
    best_distance = float('inf')

    for ref_file in reference_files:
        _, distance = verifier.verify(
            test_audio, ref_file, return_distance=True
        )

        if distance < best_distance:
            best_distance = distance
            best_match = ref_file.stem

    if best_distance < threshold:
        confidence = 1 - (best_distance / threshold)
        return best_match, confidence
    else:
        return None, 0.0

# Usage
speaker_id, conf = identify_speaker(
    "unknown_speaker.wav",
    "./reference_speakers/"
)

if speaker_id:
    print(f"Identified as: {speaker_id} (confidence: {conf:.2%})")
else:
    print("Speaker not identified")
```

## Troubleshooting

### Common Issues

**1. Audio loading errors**
```python
# Ensure audio file exists and is readable
from pathlib import Path
if not Path("audio.wav").exists():
    print("File not found!")
```

**2. CUDA/GPU issues**
```python
# Use CPU explicitly
from speech_verification.config import VerificationConfig
config = VerificationConfig(device="cpu")
```

**3. Import errors**
```bash
# Ensure package is installed
pip install -e .

# Or install all dependencies
pip install -e ".[all]"
```

## Next Steps

- 📖 Read the [full documentation](README.md)
- 🎓 Check out [advanced examples](examples/)
- 🤝 Learn how to [contribute](CONTRIBUTING.md)
- 🐛 Report [issues](https://github.com/umitkacar/Speech-Verification-Ensemble/issues)

---

Happy verifying! 🎙️✨
