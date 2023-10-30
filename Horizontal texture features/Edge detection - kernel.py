import cv2
import math
import numpy as np
from scipy import signal
from tqdm import tqdm
import matplotlib.pyplot as plt


def horizontal_textures(file_path, intensity_factor):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    kernel_horizontal = np.array([[0, 0, 0],
                       [2, -4, 2],
                       [0, 0, 0]]) * intensity_factor

    kernel_vertical = np.array([[0, 2, 0],
                       [0, -4, 0],
                       [0, 2, 0]]) * intensity_factor

    kernel_diagonal = np.array([[1, 0, 1],
                       [0, -4, 0],
                       [1, 0, 1]]) * intensity_factor
    kernel_laplacian = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]]) * (intensity_factor / 2)
    kernel_average = np.array([[1, 1, 1],
                               [1, 1, 1],
                               [1, 1, 1]]) / 9
    # kernel_average_2_by_2 = np.array([[1, 1],
    #                                   [1, 1]]) / 4


    output_kernel_horizontal = signal.correlate2d(image, kernel_horizontal) + 100
    output_kernel_horizontal_averaged = signal.correlate2d(output_kernel_horizontal, kernel_average)
    output_kernel_diagonal = signal.correlate2d(image, kernel_diagonal) + 100
    output_kernel_vertical = signal.correlate2d(image, kernel_vertical) + 100
    output_kernel_laplacian = signal.correlate2d(image, kernel_laplacian) + 100

    difference = output_kernel_laplacian - output_kernel_vertical + 100

    difference_averaged = signal.correlate2d(difference, kernel_average)


    fig1 = plt.figure(figsize=(9, 10))
    fig1.suptitle('Original Image', fontname='Times New Roman', fontweight="bold")

    ax1 = plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_horizontal, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of horizontal kernel', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_vertical, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of vertical kernel', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_laplacian, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of Laplacian kernel', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
    plt.imshow(difference, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Laplacian minus vertical', fontname='Times New Roman', fontweight="bold")

    ax6 = plt.subplot(3, 2, 6, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_horizontal_averaged, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Horizontal - Averaged', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()


    '''Blur'''

    image = signal.correlate2d(image, kernel_average)


    output_kernel_horizontal = signal.correlate2d(image, kernel_horizontal) + 100
    output_kernel_diagonal = signal.correlate2d(image, kernel_diagonal) + 100
    output_kernel_vertical = signal.correlate2d(image, kernel_vertical) + 100
    output_kernel_laplacian = signal.correlate2d(image, kernel_laplacian) + 100

    difference = output_kernel_laplacian - output_kernel_vertical + 100

    difference_averaged = signal.correlate2d(difference, kernel_average)

    fig2 = plt.figure(figsize=(9, 10))
    fig2.suptitle('Blurred Image', fontname='Times New Roman', fontweight="bold")

    ax1 = plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Blurred Image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_horizontal, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of horizontal kernel', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_vertical, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of vertical kernel', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(output_kernel_laplacian, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Output of Laplacian kernel', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
    plt.imshow(difference, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Laplacian minus vertical', fontname='Times New Roman', fontweight="bold")


    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    file_path = r'textures\1.2.12.tiff'
    horizontal_textures(file_path, intensity_factor=2)