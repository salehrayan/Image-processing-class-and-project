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
            temp[row, col] = (1 - ((row + col) % 2)) * temp[row, col]
    return temp


def minmax(array, Max):

    return (array - np.min(array)) / (np.max(array) - np.min(array)) * Max


def filtering_in_fourier(file1_path, standard_deviation):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    x_temp = np.arange(-height + 1, height + 1)
    y_temp = np.arange(-width + 1, width + 1)
    Y, X = np.meshgrid(y_temp, x_temp)
    filter_gaussian = (minmax(np.exp(-(X**2 + Y**2)/(2 * standard_deviation**2))/(2 * np.pi *
                                                                                          standard_deviation**2),
                                      Max=1))
    # plt.imshow(filter_gaussian, cmap='gray', vmin=0, vmax=255)
    # plt.show()

    image_zero_padded_fft = np.fft.fft2(fftshift_in_time(image), s=(height*2, width*2))
    image_fft_filtered = image_zero_padded_fft * filter_gaussian
    plt.imshow(np.real(np.fft.ifft2(np.fft.ifftshift(image_fft_filtered))), cmap='gray', vmin=0, vmax=255)
    plt.show()

if __name__ == "__main__":
    file1 = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lena_gray_512.tif'

    filtering_in_fourier(file1, standard_deviation=15)
