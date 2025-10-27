"""
Runner module for executing the BM3D algorithm.
"""

import os
from typing import List
import numpy as np
from .dataset import DatasetLoader
from .metrics import calculate_psnr, calculate_ssim
from .bm3d import bm3d_rgb  # Assume this is the BM3D implementation

class BM3DRunner:
    """
    A class to run the BM3D algorithm on a dataset.
    """

    def __init__(self, data_dir: str, results_dir: str, noise_sigma: float):
        """
        Initialize the runner.
        :param data_dir: Path to the dataset directory.
        :param results_dir: Path to save the results.
        :param noise_sigma: Standard deviation of the noise.
        """
        self.dataset_loader = DatasetLoader(data_dir)
        self.results_dir = results_dir
        self.noise_sigma = noise_sigma
        os.makedirs(results_dir, exist_ok=True)

    def run(self):
        """
        Run the BM3D algorithm on the dataset.
        """
        # Load dataset
        original_images = self.dataset_loader.load_images()
        noisy_images = self.dataset_loader.add_noise(original_images, self.noise_sigma)

        psnr_values = []
        ssim_values = []

        # Process each image
        for i, (original, noisy) in enumerate(zip(original_images, noisy_images)):
            # Apply BM3D algorithm
            denoised = bm3d_rgb(noisy, self.noise_sigma)

            # Save results
            save_path = os.path.join(self.results_dir, f"denoised_{i}.png")
            cv2.imwrite(save_path, denoised)

            # Calculate metrics
            psnr_value = calculate_psnr(original, denoised)
            ssim_value = calculate_ssim(original, denoised)
            psnr_values.append(psnr_value)
            ssim_values.append(ssim_value)

            print(f"Image {i}: PSNR={psnr_value:.2f}, SSIM={ssim_value:.4f}")

        # Print average metrics
        print(f"Average PSNR: {np.mean(psnr_values):.2f}")
        print(f"Average SSIM: {np.mean(ssim_values):.4f}")