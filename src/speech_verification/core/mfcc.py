"""MFCC + DTW-based speaker verification."""

import logging
from pathlib import Path
from typing import Optional, Union

import librosa
import numpy as np
from dtw import dtw
from numpy.linalg import norm

from speech_verification.config import AudioConfig, VerificationConfig
from speech_verification.utils.audio import load_audio

logger = logging.getLogger(__name__)


class MFCCVerifier:
    """
    MFCC + Dynamic Time Warping speaker verification.

    This class implements traditional signal processing approach for
    speaker verification using Mel-Frequency Cepstral Coefficients (MFCC)
    and Dynamic Time Warping (DTW) for temporal alignment.

    Attributes:
        audio_config: Audio processing configuration
        verification_config: Verification thresholds
        threshold: Distance threshold for verification
    """

    def __init__(
        self,
        audio_config: Optional[AudioConfig] = None,
        verification_config: Optional[VerificationConfig] = None,
    ) -> None:
        """
        Initialize MFCC verifier.

        Args:
            audio_config: Audio processing configuration
            verification_config: Verification configuration
        """
        self.audio_config = audio_config or AudioConfig()
        self.verification_config = verification_config or VerificationConfig()
        self.threshold = self.verification_config.mfcc_threshold
        logger.info(f"Initialized MFCCVerifier with threshold={self.threshold}")

    def extract_mfcc(
        self, audio_path: Union[str, Path], y: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Extract MFCC features from audio.

        Args:
            audio_path: Path to audio file
            y: Pre-loaded audio array (optional)

        Returns:
            MFCC feature matrix (n_mfcc, n_frames)
        """
        if y is None:
            y, sr = load_audio(audio_path, sr=self.audio_config.sample_rate)
        else:
            sr = self.audio_config.sample_rate

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=self.audio_config.n_mfcc,
            n_fft=self.audio_config.n_fft,
            hop_length=self.audio_config.hop_length,
        )

        logger.debug(f"Extracted MFCC features: shape={mfcc.shape}")
        return mfcc

    def compute_distance(self, mfcc1: np.ndarray, mfcc2: np.ndarray) -> float:
        """
        Compute DTW distance between two MFCC feature matrices.

        Args:
            mfcc1: First MFCC matrix
            mfcc2: Second MFCC matrix

        Returns:
            DTW distance (lower = more similar)
        """
        dist, cost, acc_cost, path = dtw(
            mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=2)
        )
        logger.debug(f"DTW distance computed: {dist:.2f}")
        return float(dist)

    def verify(
        self,
        audio1: Union[str, Path],
        audio2: Union[str, Path],
        return_distance: bool = False,
    ) -> Union[bool, tuple[bool, float]]:
        """
        Verify if two audio samples are from the same speaker.

        Args:
            audio1: Path to first audio file
            audio2: Path to second audio file
            return_distance: If True, also return the distance

        Returns:
            Boolean verification result, optionally with distance
        """
        logger.info(f"Verifying: {audio1} vs {audio2}")

        mfcc1 = self.extract_mfcc(audio1)
        mfcc2 = self.extract_mfcc(audio2)

        distance = self.compute_distance(mfcc1, mfcc2)
        is_same_speaker = distance < self.threshold

        logger.info(
            f"MFCC Distance: {distance:.2f}, "
            f"Threshold: {self.threshold}, "
            f"Same Speaker: {is_same_speaker}"
        )

        if return_distance:
            return is_same_speaker, distance
        return is_same_speaker

    def batch_verify(
        self, audio_pairs: list[tuple[Union[str, Path], Union[str, Path]]]
    ) -> list[tuple[bool, float]]:
        """
        Verify multiple audio pairs.

        Args:
            audio_pairs: List of (audio1, audio2) tuples

        Returns:
            List of (is_same_speaker, distance) tuples
        """
        results = []
        for audio1, audio2 in audio_pairs:
            result = self.verify(audio1, audio2, return_distance=True)
            results.append(result)
        return results
