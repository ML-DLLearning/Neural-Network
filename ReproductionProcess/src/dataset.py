"""
Dataset processing module for BM3D algorithm reproduction.
"""

import os
import cv2
import numpy as np
from typing import List, Tuple

class DatasetLoader:
    """
    A class to handle dataset loading and preprocessing for BM3D algorithm.
    """

    def __init__(self, data_dir: str):
        """
        Initialize the dataset loader.
        :param data_dir: Path to the dataset directory.
        """
        self.data_dir = data_dir

    def load_images(self, extensions: Tuple[str, ...] = (".png", ".jpg")) -> List[np.ndarray]:
        """
        Load images from the dataset directory.
        :param extensions: Allowed image extensions.
        :return: List of images as NumPy arrays.
        """
        images = []
        for file_name in os.listdir(self.data_dir):
            if file_name.endswith(extensions):
                img_path = os.path.join(self.data_dir, file_name)
                image = cv2.imread(img_path)
                if image is not None:
                    images.append(image)
        return images

    def add_noise(self, images: List[np.ndarray], sigma: float) -> List[np.ndarray]:
        """
        Add Gaussian noise to the images.
        :param images: List of images as NumPy arrays.
        :param sigma: Standard deviation of the Gaussian noise.
        :return: List of noisy images.
        """
        noisy_images = []
        for image in images:
            noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
            noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
            noisy_images.append(noisy_image)
        return noisy_images