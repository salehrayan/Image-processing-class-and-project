import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt

np.random.seed(42)

def noise_remove(file_path, intensity_factor, std, averaging_kernel_dim, rec_factor):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)


    kernel_vertical = np.array([[0, 0, 0],
                       [2, -4, 2],
                       [0, 0, 0]]) * intensity_factor

    kernel_horizontal = np.array([[0, 2, 0],
                       [0, -4, 0],
                       [0, 2, 0]]) * intensity_factor

    kernel_laplacian = np.array([[1, 0, 1],
                       [0, -4, 0],
                       [1, 0, 1]]) * intensity_factor
    kernel_diagonal = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]]) * (intensity_factor / 2)
    kernel_average = np.ones((averaging_kernel_dim, averaging_kernel_dim)) / (averaging_kernel_dim**2)

    image_blur = signal.correlate2d(image, kernel_average, boundary='symm')
    image_blur_noise = image_blur + std* np.random.randn(image_blur.shape[0], image_blur.shape[1])

    image_laplacian = signal.correlate2d(image_blur_noise, kernel_laplacian, boundary='symm')
    image_section = image_blur_noise[884:946, 418:872].copy()
    std_estimate = np.std(image_section.reshape(-1))
    print(std_estimate)

    image_section_accumulation = image_section.copy()

    for i in range(5000):
        image_section_accumulation = (image_section_accumulation +
                                      (image_section_accumulation +
            std_estimate * np.random.randn(image_section_accumulation.shape[0], image_section_accumulation.shape[1])))/2


    image_section_accumulation = (image_section_accumulation - np.min(image_section_accumulation))/(
        np.max(image_section_accumulation) - np.min(image_section_accumulation)
    ) * 255
    print(np.std(image_section_accumulation.reshape(-1)))
    print(np.mean(image_section_accumulation.reshape(-1)))

    fig1 = plt.figure(figsize=(9, 9))

    ax1 = plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Original image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(image_blur_noise, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Degraded image', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(image_laplacian, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Image Laplacian', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(3, 2, 4)
    plt.hist(image_section.reshape(-1), bins=256)
    plt.xlim([0, 255])
    plt.title(f'Histogram of section', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(3, 2, 5)
    plt.hist(image_section_accumulation.reshape(-1), bins=256)
    plt.xlim([0, 255])
    plt.title(f'Histogram of noise removed section', fontname='Times New Roman', fontweight="bold")

    ax6 = plt.subplot(3, 2, 6)
    plt.imshow(image_section_accumulation, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Reconstructed Image', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.02.tiff'
    noise_remove(file_path, intensity_factor=1, std=40, averaging_kernel_dim=4, rec_factor=-0.15)