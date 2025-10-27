import numpy as np
from bm3d import bm3d_rgb, BM3DProfile
from experiment_funcs import get_experiment_noise, get_psnr, get_cropped_psnr
from PIL import Image
import matplotlib.pyplot as plt


def load_image(image_path):
    """Load an image and normalize to [0, 1]. Ensure it's in RGB format."""
    try:
        img = Image.open(image_path)
        # 如果图像是 RGBA，去掉透明通道
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # 如果图像是灰度图像，转换为 RGB
        elif img.mode == 'L':
            img = img.convert('RGB')
        # 确保图像为 RGB
        if img.mode != 'RGB':
            raise ValueError("Input image must be 3-channel RGB or grayscale.")
        return np.array(img) / 255
    except Exception as e:
        raise ValueError(f"Failed to load image from `{image_path}`. Error: {e}")


def add_noise(y, noise_type, noise_var, seed):
    """Generate noise and add it to the image."""
    noise, psd, kernel = get_experiment_noise(noise_type, noise_var, seed, y.shape)
    z = np.atleast_3d(y) + np.atleast_3d(noise)
    return z, psd


def display_and_save_results(y, z, y_est, output_path):
    """Display results and save the denoised image."""
    # Ignore values outside range for display
    y_est = np.minimum(np.maximum(y_est, 0), 1)
    z_rang = np.minimum(np.maximum(z, 0), 1)

    # Display images
    plt.title("Original, Noisy, Denoised")
    plt.imshow(np.concatenate((y, np.squeeze(z_rang), y_est), axis=1))
    plt.show()

    # Save the denoised image
    denoised_image = (y_est * 255).astype(np.uint8)
    Image.fromarray(denoised_image).save(output_path)
    print(f"Denoised image saved to `{output_path}`")


def main():
    # Hardcoded paths for input and output (adjust as needed)
    image_path = r"your image path"
    output_path = r"define yourself"

    # Noise parameters

    noise_type = "g3"
    noise_var = 0.02
    seed = 0

    # Load the noise-free image
    y = load_image(image_path)
    print(f"Original image shape: {y.shape}")

    # Add noise to the image
    z, psd = add_noise(y, noise_type, noise_var, seed)
    print(f"Noisy image shape: {z.shape}")

    # Apply BM3D denoising
    y_est = bm3d_rgb(z, psd)

    # Compute PSNR
    psnr = get_psnr(y, y_est)
    print("PSNR:", psnr)

    # Compute cropped PSNR
    psnr_cropped = get_cropped_psnr(y, y_est, [16, 16])
    print("PSNR cropped:", psnr_cropped)

    # Display and save results
    display_and_save_results(y, z, y_est, output_path)


if __name__ == '__main__':
    main()