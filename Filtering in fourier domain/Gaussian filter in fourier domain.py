import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt


def fftshift_in_time(x):
    temp = x.copy()
    for row in range(temp.shape[0]):
        for col in range(temp.shape[1]):
            temp[row, col] = (-1) ** (row + col) * temp[row, col]
    return temp


def minmax(array, Max):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * Max


def filtering_in_fourier(file1_path, standard_deviation):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    x_temp = np.linspace(-height / 2, height / 2, height * 2)
    y_temp = np.linspace(-width / 2, width / 2, width * 2)
    Y, X = np.meshgrid(y_temp, x_temp)
    filter_gaussian = np.exp(-(X ** 2 + Y ** 2) / (2 * standard_deviation ** 2))

    image_zero_padded_fft = np.fft.fft2(fftshift_in_time(image), s=(height * 2, width * 2))
    image_fft_filtered = image_zero_padded_fft * filter_gaussian
    image_zero_padded_filtered = np.real(np.fft.ifft2(np.fft.ifftshift(image_fft_filtered)))
    image_zero_padded_filtered[0:height, 0:width] = image_zero_padded_filtered[0:height, 0:width] + \
                                                    (np.mean(image)
                                                     - np.mean(image_zero_padded_filtered[0:height, 0:width]))

    fig = plt.figure(figsize=(11, 10))
    ax1 = plt.subplot(231)
    ax1.imshow(image, cmap='gray', vmin=0, vmax=255)
    ax1.set_title('Original Image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(232)
    ax2.imshow(np.real(np.fft.ifft2(np.fft.ifftshift(image_zero_padded_fft))), cmap='gray', vmin=0, vmax=255)
    ax2.set_title(f'Zero-padded image', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(233)
    ax3.imshow(np.log(np.abs(image_zero_padded_fft) + 1) ** 2, cmap='gray', vmin=0, vmax=255)
    ax3.set_title(f'FFT of zero-padded image', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(2, 3, 4)
    ax4.imshow(filter_gaussian, cmap='gray', vmin=0, vmax=1)
    ax4.set_title(f'Gaussian filter, std = {standard_deviation}', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(2, 3, 5)
    ax5.imshow(np.log(np.abs(image_fft_filtered) + 1) ** 2, cmap='gray', vmin=0, vmax=255)
    ax5.set_title(f'Filtered FFT', fontname='Times New Roman', fontweight="bold")

    ax6 = plt.subplot(2, 3, 6)
    ax6.imshow(image_zero_padded_filtered, cmap='gray', vmin=0, vmax=255)
    ax6.set_title(f'Zero-padded filtered image', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()

    plt.figure()
    plt.imshow(image_zero_padded_filtered[0:height, 0:width], cmap='gray', vmin=0,
               vmax=255)
    plt.title('Final image', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file1 = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\livingroom.tif'

    filtering_in_fourier(file1, standard_deviation=20)
