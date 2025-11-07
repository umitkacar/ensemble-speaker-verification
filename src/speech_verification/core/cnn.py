"""CNN-based speaker verification using Resemblyzer."""

import logging
from pathlib import Path
from typing import Optional, Union

import numpy as np
from numpy.linalg import norm
from resemblyzer import VoiceEncoder, preprocess_wav

from speech_verification.config import VerificationConfig
from speech_verification.utils.audio import load_audio

logger = logging.getLogger(__name__)


class CNNVerifier:
    """
    CNN-based speaker verification using Resemblyzer.

    This class uses a pre-trained deep learning model (Resemblyzer)
    for speaker verification. It extracts 256-dimensional speaker
    embeddings and compares them using Euclidean distance.

    Attributes:
        encoder: Resemblyzer VoiceEncoder
        verification_config: Verification configuration
        threshold: Distance threshold for verification
    """

    def __init__(
        self,
        verification_config: Optional[VerificationConfig] = None,
        device: Optional[str] = None,
    ) -> None:
        """
        Initialize CNN verifier.

        Args:
            verification_config: Verification configuration
            device: Device to use ('cpu' or 'cuda')
        """
        self.verification_config = verification_config or VerificationConfig()
        device = device or self.verification_config.device
        self.threshold = self.verification_config.cnn_threshold

        logger.info(f"Loading Resemblyzer encoder on device: {device}")
        self.encoder = VoiceEncoder(device=device)
        logger.info(
            f"Initialized CNNVerifier with threshold={self.threshold}"
        )

    def extract_embedding(
        self, audio_path: Union[str, Path]
    ) -> np.ndarray:
        """
        Extract speaker embedding from audio.

        Args:
            audio_path: Path to audio file

        Returns:
            256-dimensional speaker embedding
        """
        wav = preprocess_wav(Path(audio_path))
        embedding = self.encoder.embed_utterance(wav)

        logger.debug(
            f"Extracted embedding: shape={embedding.shape}, "
            f"norm={norm(embedding):.3f}"
        )
        return embedding

    def compute_distance(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        """
        Compute Euclidean distance between embeddings.

        Args:
            embedding1: First speaker embedding
            embedding2: Second speaker embedding

        Returns:
            Euclidean distance (lower = more similar)
        """
        distance = float(norm(embedding1 - embedding2))
        logger.debug(f"Embedding distance computed: {distance:.4f}")
        return distance

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

        embedding1 = self.extract_embedding(audio1)
        embedding2 = self.extract_embedding(audio2)

        distance = self.compute_distance(embedding1, embedding2)
        is_same_speaker = distance < self.threshold

        logger.info(
            f"CNN Distance: {distance:.4f}, "
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

    def compare_multiple(
        self, reference: Union[str, Path], candidates: list[Union[str, Path]]
    ) -> list[tuple[Path, float, bool]]:
        """
        Compare reference audio against multiple candidates.

        Args:
            reference: Reference audio path
            candidates: List of candidate audio paths

        Returns:
            List of (path, distance, is_same_speaker) tuples, sorted by distance
        """
        ref_embedding = self.extract_embedding(reference)
        results = []

        for candidate in candidates:
            cand_embedding = self.extract_embedding(candidate)
            distance = self.compute_distance(ref_embedding, cand_embedding)
            is_same = distance < self.threshold
            results.append((Path(candidate), distance, is_same))

        # Sort by distance (ascending)
        results.sort(key=lambda x: x[1])
        return results
