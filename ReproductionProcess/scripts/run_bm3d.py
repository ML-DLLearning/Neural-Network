"""
Run BM3D algorithm on noisy images.
"""

import os
import cv2
import numpy as np
from src.bm3d import bm3d_rgb

def run_bm3d(input_dir: str, output_dir: str, noise_std: float):
    """
    Run BM3D algorithm on noisy images and save the results.
    :param input_dir: Path to the noisy images directory.
    :param output_dir: Path to save denoised images.
    :param noise_std: Noise standard deviation.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, file_name)
            noisy_image = cv2.imread(image_path)
            if noisy_image is not None:
                denoised_image = bm3d_rgb(noisy_image, noise_std)
                output_path = os.path.join(output_dir, f"denoised_{file_name}")
                cv2.imwrite(output_path, denoised_image)
                print(f"Saved denoised image to {output_path}")

# Example usage
if __name__ == "__main__":
    input_dir = "data/noisy_images"
    output_dir = "results/denoised_images"
    noise_std = 25
    run_bm3d(input_dir, output_dir, noise_std)