"""Ensemble fusion for combining MFCC and CNN verifiers."""

import logging
from pathlib import Path
from typing import Optional, Union

import numpy as np

from speech_verification.config import VerificationConfig
from speech_verification.core.cnn import CNNVerifier
from speech_verification.core.mfcc import MFCCVerifier

logger = logging.getLogger(__name__)


class EnsembleVerifier:
    """
    Ensemble verifier combining MFCC and CNN approaches.

    This class implements score-level fusion to combine the strengths
    of both MFCC + DTW and CNN-based verification methods.

    Attributes:
        mfcc_verifier: MFCC + DTW verifier
        cnn_verifier: CNN verifier
        weight_cnn: Weight for CNN scores (default: 0.7)
        weight_mfcc: Weight for MFCC scores (default: 0.3)
    """

    def __init__(
        self,
        mfcc_verifier: Optional[MFCCVerifier] = None,
        cnn_verifier: Optional[CNNVerifier] = None,
        verification_config: Optional[VerificationConfig] = None,
    ) -> None:
        """
        Initialize ensemble verifier.

        Args:
            mfcc_verifier: MFCC verifier instance
            cnn_verifier: CNN verifier instance
            verification_config: Verification configuration
        """
        self.verification_config = verification_config or VerificationConfig()

        self.mfcc_verifier = mfcc_verifier or MFCCVerifier(
            verification_config=self.verification_config
        )
        self.cnn_verifier = cnn_verifier or CNNVerifier(
            verification_config=self.verification_config
        )

        self.weight_cnn = self.verification_config.fusion_weight_cnn
        self.weight_mfcc = self.verification_config.fusion_weight_mfcc

        logger.info(
            f"Initialized EnsembleVerifier with weights: "
            f"CNN={self.weight_cnn}, MFCC={self.weight_mfcc}"
        )

    @staticmethod
    def tanh_normalize(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Apply tanh normalization to scores.

        Formula: normalized(x) = 0.5 * (tanh(0.01 * (x - μ) / σ) + 1)

        Args:
            x: Score or array of scores

        Returns:
            Normalized score(s) in [0, 1]
        """
        x_array = np.atleast_1d(x)
        mean = np.mean(x_array)
        std = np.std(x_array)

        if std == 0:
            return 0.5 if isinstance(x, (int, float)) else np.full_like(x_array, 0.5)

        normalized = 0.5 * (np.tanh(0.01 * ((x_array - mean) / std)) + 1)

        if isinstance(x, (int, float)):
            return float(normalized[0])
        return normalized

    def verify(
        self,
        audio1: Union[str, Path],
        audio2: Union[str, Path],
        return_details: bool = False,
    ) -> Union[bool, dict]:
        """
        Verify using ensemble fusion.

        Args:
            audio1: Path to first audio file
            audio2: Path to second audio file
            return_details: If True, return detailed results

        Returns:
            Boolean verification result or detailed dict
        """
        logger.info(f"Ensemble verification: {audio1} vs {audio2}")

        # Get individual verifier results
        mfcc_result, mfcc_dist = self.mfcc_verifier.verify(
            audio1, audio2, return_distance=True
        )
        cnn_result, cnn_dist = self.cnn_verifier.verify(
            audio1, audio2, return_distance=True
        )

        # Normalize scores
        mfcc_normalized = self.tanh_normalize(mfcc_dist)
        cnn_normalized = self.tanh_normalize(cnn_dist)

        # Compute fusion score
        fusion_score = (
            self.weight_cnn * cnn_normalized + self.weight_mfcc * mfcc_normalized
        )

        # Determine if same speaker using OR logic
        # (same if either method says same)
        is_same_speaker = mfcc_result or cnn_result

        logger.info(
            f"MFCC: {mfcc_result} (dist={mfcc_dist:.2f}, norm={mfcc_normalized:.4f})"
        )
        logger.info(
            f"CNN: {cnn_result} (dist={cnn_dist:.4f}, norm={cnn_normalized:.4f})"
        )
        logger.info(
            f"Fusion score: {fusion_score:.4f}, Same speaker: {is_same_speaker}"
        )

        if return_details:
            return {
                "is_same_speaker": is_same_speaker,
                "fusion_score": float(fusion_score),
                "mfcc": {
                    "result": mfcc_result,
                    "distance": float(mfcc_dist),
                    "normalized": float(mfcc_normalized),
                    "threshold": self.mfcc_verifier.threshold,
                },
                "cnn": {
                    "result": cnn_result,
                    "distance": float(cnn_dist),
                    "normalized": float(cnn_normalized),
                    "threshold": self.cnn_verifier.threshold,
                },
                "weights": {
                    "cnn": self.weight_cnn,
                    "mfcc": self.weight_mfcc,
                },
            }

        return is_same_speaker

    def batch_verify(
        self, audio_pairs: list[tuple[Union[str, Path], Union[str, Path]]]
    ) -> list[dict]:
        """
        Verify multiple audio pairs with ensemble.

        Args:
            audio_pairs: List of (audio1, audio2) tuples

        Returns:
            List of detailed verification results
        """
        results = []
        for audio1, audio2 in audio_pairs:
            result = self.verify(audio1, audio2, return_details=True)
            results.append(result)
        return results

    def optimize_weights(
        self,
        audio_pairs: list[tuple[Union[str, Path], Union[str, Path]]],
        labels: list[bool],
        weight_range: tuple[float, float] = (0.0, 1.0),
        step: float = 0.1,
    ) -> tuple[float, float, float]:
        """
        Optimize fusion weights using grid search.

        Args:
            audio_pairs: List of (audio1, audio2) tuples
            labels: Ground truth labels (True = same speaker)
            weight_range: Range of weights to search
            step: Step size for grid search

        Returns:
            Tuple of (best_cnn_weight, best_mfcc_weight, best_accuracy)
        """
        logger.info("Optimizing fusion weights...")

        best_accuracy = 0.0
        best_cnn_weight = self.weight_cnn
        best_mfcc_weight = self.weight_mfcc

        weights = np.arange(weight_range[0], weight_range[1] + step, step)

        for cnn_weight in weights:
            mfcc_weight = 1.0 - cnn_weight

            # Temporarily set weights
            self.weight_cnn = cnn_weight
            self.weight_mfcc = mfcc_weight

            # Verify all pairs
            predictions = [
                self.verify(audio1, audio2) for audio1, audio2 in audio_pairs
            ]

            # Calculate accuracy
            correct = sum(pred == label for pred, label in zip(predictions, labels))
            accuracy = correct / len(labels)

            logger.debug(
                f"CNN weight: {cnn_weight:.2f}, "
                f"MFCC weight: {mfcc_weight:.2f}, "
                f"Accuracy: {accuracy:.4f}"
            )

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_cnn_weight = cnn_weight
                best_mfcc_weight = mfcc_weight

        # Set optimal weights
        self.weight_cnn = best_cnn_weight
        self.weight_mfcc = best_mfcc_weight

        logger.info(
            f"Optimal weights found: CNN={best_cnn_weight:.2f}, "
            f"MFCC={best_mfcc_weight:.2f}, Accuracy={best_accuracy:.4f}"
        )

        return best_cnn_weight, best_mfcc_weight, best_accuracy
