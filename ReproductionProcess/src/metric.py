"""
Metrics module for evaluating the BM3D algorithm.
"""

import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(original: np.ndarray, denoised: np.ndarray) -> float:
    """
    Calculate PSNR (Peak Signal-to-Noise Ratio) between two images.
    :param original: The original clean image.
    :param denoised: The denoised image.
    :return: PSNR value.
    """
    return psnr(original, denoised, data_range=original.max() - original.min())

def calculate_ssim(original: np.ndarray, denoised: np.ndarray) -> float:
    """
    Calculate SSIM (Structural Similarity Index) between two images.
    :param original: The original clean image.
    :param denoised: The denoised image.
    :return: SSIM value.
    """
    return ssim(original, denoised, multichannel=True)