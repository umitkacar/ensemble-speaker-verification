"""Audio processing utilities."""

import logging
from pathlib import Path
from typing import Optional, Union

import librosa
import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)


def load_audio(
    audio_path: Union[str, Path], sr: int = 16000, mono: bool = True
) -> tuple[np.ndarray, int]:
    """
    Load audio file with librosa.

    Args:
        audio_path: Path to audio file
        sr: Target sample rate
        mono: Convert to mono if True

    Returns:
        Tuple of (audio_array, sample_rate)

    Raises:
        FileNotFoundError: If audio file doesn't exist
        RuntimeError: If audio loading fails
    """
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        y, sample_rate = librosa.load(str(audio_path), sr=sr, mono=mono)
        logger.debug(
            f"Loaded audio: {audio_path.name}, " f"shape={y.shape}, sr={sample_rate}"
        )
        return y, sample_rate
    except Exception as e:
        raise RuntimeError(f"Failed to load audio {audio_path}: {e}") from e


def convert_audio(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    sr: int = 16000,
    format: Optional[str] = None,
) -> Path:
    """
    Convert audio file to different format/sample rate.

    Args:
        input_path: Input audio file path
        output_path: Output audio file path
        sr: Target sample rate
        format: Output format (inferred from extension if None)

    Returns:
        Path to converted audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        RuntimeError: If conversion fails
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        # Load audio
        y, _ = load_audio(input_path, sr=sr)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save with soundfile
        if format is None:
            format = output_path.suffix.lstrip(".")

        sf.write(str(output_path), y, sr, format=format)

        logger.info(f"Converted {input_path.name} -> {output_path.name}")
        return output_path

    except Exception as e:
        raise RuntimeError(
            f"Failed to convert audio {input_path} -> {output_path}: {e}"
        ) from e


def record_audio(
    output_path: Union[str, Path],
    duration: int = 5,
    sr: int = 16000,
    channels: int = 1,
) -> Path:
    """
    Record audio from microphone.

    Args:
        output_path: Path to save recorded audio
        duration: Recording duration in seconds
        sr: Sample rate
        channels: Number of channels (1=mono, 2=stereo)

    Returns:
        Path to recorded audio file

    Raises:
        RuntimeError: If recording fails
    """
    output_path = Path(output_path)

    try:
        import sounddevice as sd

        logger.info(f"Recording for {duration} seconds...")
        audio = sd.rec(
            int(duration * sr), samplerate=sr, channels=channels, dtype="float32"
        )
        sd.wait()

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save audio
        sf.write(str(output_path), audio, sr)
        logger.info(f"Audio saved to {output_path}")

        return output_path

    except ImportError:
        raise RuntimeError(
            "sounddevice not installed. Install with: pip install sounddevice"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to record audio: {e}") from e


def normalize_audio(y: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    """
    Normalize audio to target loudness.

    Args:
        y: Audio array
        target_db: Target loudness in dB

    Returns:
        Normalized audio array
    """
    # Calculate current RMS
    rms = np.sqrt(np.mean(y**2))

    # Convert target from dB to linear
    target_rms = 10 ** (target_db / 20)

    # Apply gain
    if rms > 0:
        gain = target_rms / rms
        y_normalized = y * gain
    else:
        y_normalized = y

    return y_normalized


def trim_silence(
    y: np.ndarray, sr: int, top_db: int = 30
) -> tuple[np.ndarray, tuple[int, int]]:
    """
    Trim leading and trailing silence from audio.

    Args:
        y: Audio array
        sr: Sample rate
        top_db: Threshold in dB below reference

    Returns:
        Tuple of (trimmed_audio, (start_sample, end_sample))
    """
    y_trimmed, (start, end) = librosa.effects.trim(y, top_db=top_db)
    logger.debug(f"Trimmed silence: {start} -> {end} samples")
    return y_trimmed, (start, end)
