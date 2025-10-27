"""
Evaluate denoised images using PSNR and SSIM metrics.
"""

import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def evaluate_images(original_dir: str, denoised_dir: str):
    """
    Evaluate denoised images by calculating PSNR and SSIM metrics.
    :param original_dir: Path to the original images directory.
    :param denoised_dir: Path to the denoised images directory.
    """
    original_files = sorted(os.listdir(original_dir))
    denoised_files = sorted(os.listdir(denoised_dir))

    psnr_values = []
    ssim_values = []

    for original_file, denoised_file in zip(original_files, denoised_files):
        original_path = os.path.join(original_dir, original_file)
        denoised_path = os.path.join(denoised_dir, denoised_file)

        original_image = cv2.imread(original_path)
        denoised_image = cv2.imread(denoised_path)

        if original_image is not None and denoised_image is not None:
            psnr_value = psnr(original_image, denoised_image, data_range=original_image.max() - original_image.min())
            ssim_value = ssim(original_image, denoised_image, multichannel=True)
            psnr_values.append(psnr_value)
            ssim_values.append(ssim_value)
            print(f"Image: {original_file}, PSNR: {psnr_value:.2f}, SSIM: {ssim_value:.4f}")

    print(f"Average PSNR: {np.mean(psnr_values):.2f}")
    print(f"Average SSIM: {np.mean(ssim_values):.4f}")

# Example usage
if __name__ == "__main__":
    original_dir = "data/original_images"
    denoised_dir = "results/denoised_images"
    evaluate_images(original_dir, denoised_dir)