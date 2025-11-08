"""Configuration management for speech verification."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class AudioConfig:
    """Audio processing configuration."""

    sample_rate: int = 16000
    n_mfcc: int = 13
    n_fft: int = 2048
    hop_length: int = 512
    supported_formats: tuple[str, ...] = (".wav", ".mp3", ".ogg", ".flac", ".m4a")


@dataclass
class VerificationConfig:
    """Verification thresholds and parameters."""

    mfcc_threshold: float = 9000.0
    cnn_threshold: float = 0.80
    fusion_weight_cnn: float = 0.7
    fusion_weight_mfcc: float = 0.3
    device: str = "cpu"  # "cpu" or "cuda"


@dataclass
class Config:
    """Main configuration container."""

    audio: AudioConfig = field(default_factory=AudioConfig)
    verification: VerificationConfig = field(default_factory=VerificationConfig)
    data_dir: Path = field(default_factory=lambda: Path("./data"))
    output_dir: Path = field(default_factory=lambda: Path("./output"))
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Ensure directories exist."""
        self.data_dir = Path(self.data_dir)
        self.output_dir = Path(self.output_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


# Global default configuration
DEFAULT_CONFIG = Config()
