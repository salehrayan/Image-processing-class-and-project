import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt


def noise_remove(file_path, intensity_factor, std, averaging_kernel_dim, rec_factor):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    image_noisy = image + (std* np.random.randn(image.shape[0], image.shape[1]))

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

    kernel_average_2 = np.ones((4, 4))/9

    output_kernel_vertical_noise = signal.correlate2d(image_noisy, kernel_vertical, boundary='symm')
    output_kernel_diagonal_noise = signal.correlate2d(image_noisy, kernel_diagonal, boundary='symm')
    output_kernel_horizontal_noise = signal.correlate2d(image_noisy, kernel_horizontal, boundary='symm')
    output_kernel_laplacian_noise = signal.correlate2d(image_noisy, kernel_laplacian, boundary='symm')

    difference_noise = output_kernel_laplacian_noise - output_kernel_horizontal_noise

    difference_averaged_noise = signal.correlate2d(difference_noise, kernel_average, boundary='symm')


    '''Blur'''
    image_noisy_blur = signal.correlate2d(image_noisy, kernel_average)

    output_kernel_vertical_blur = signal.correlate2d(image_noisy_blur, kernel_vertical, boundary='symm')
    output_kernel_diagonal_blur = signal.correlate2d(image_noisy_blur, kernel_diagonal, boundary='symm')
    output_kernel_horizontal_blur = signal.correlate2d(image_noisy_blur, kernel_horizontal, boundary='symm')
    output_kernel_laplacian_blur = signal.correlate2d(image_noisy_blur, kernel_laplacian, boundary='symm')

    difference_blur = output_kernel_laplacian_blur - output_kernel_horizontal_blur

    difference_averaged_blur = signal.correlate2d(difference_blur, kernel_average, boundary='symm')

    output_kernel_laplacian_blur_averaged = signal.correlate2d(output_kernel_laplacian_blur, kernel_average_2,
                                             boundary='symm')

    reconstruction_image = image_noisy_blur + rec_factor*output_kernel_laplacian_blur[1:image.shape[0]+5, 1:image.shape[0]+5]


    fig1 = plt.figure(figsize=(9, 10))

    ax1 = plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Original image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(image_noisy, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Noisy image', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(image_noisy_blur, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Noisy blurred Image', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_laplacian_noise, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Laplacian of noisy image', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_laplacian_blur, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Laplacian of blurred noisy image', fontname='Times New Roman', fontweight="bold")

    ax6 = plt.subplot(3, 2, 6, sharex=ax1, sharey=ax1)
    plt.imshow(reconstruction_image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Reconstructed Image', fontname='Times New Roman', fontweight="bold")

    # plt.tight_layout()
    #
    # fig2 = plt.figure(figsize=(9, 10))
    # ax1 = plt.subplot(2, 1, 1, sharex=ax1, sharey=ax1)
    # plt.imshow(reconstruction_image2, cmap='gray', vmax=255, vmin=0)
    # plt.title(f'Reconstructed Image 2', fontname='Times New Roman', fontweight="bold")


    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.02.tiff'
    noise_remove(file_path, intensity_factor=2, std=50, averaging_kernel_dim=5, rec_factor=-0.15)