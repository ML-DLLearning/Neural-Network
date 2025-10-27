"""
Generate noisy images from the dataset.
"""

import os
import numpy as np
import cv2
from typing import List

def add_noise(image: np.ndarray, noise_std: float) -> np.ndarray:
    """
    Add Gaussian noise to an image.
    :param image: Original image (HxWxC).
    :param noise_std: Noise standard deviation.
    :return: Noisy image.
    """
    noise = np.random.normal(0, noise_std, image.shape).astype(np.float32)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image

def generate_noisy_images(input_dir: str, output_dir: str, noise_std: float):
    """
    Generate noisy images from the dataset in the input directory.
    :param input_dir: Path to the original images directory.
    :param output_dir: Path to save noisy images.
    :param noise_std: Noise standard deviation.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, file_name)
            image = cv2.imread(image_path)
            if image is not None:
                noisy_image = add_noise(image, noise_std)
                output_path = os.path.join(output_dir, f"noisy_{file_name}")
                cv2.imwrite(output_path, noisy_image)
                print(f"Saved noisy image to {output_path}")

# Example usage
if __name__ == "__main__":
    input_dir = "data/original_images"
    output_dir = "data/noisy_images"
    noise_std = 25
    generate_noisy_images(input_dir, output_dir, noise_std)