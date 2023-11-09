import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt
from skimage import restoration


def inverse_fourier(file1_path, file2_path, intensity_factor):
    image1 = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(file2_path, cv2.IMREAD_GRAYSCALE)

    image1_fft = np.fft.fft2(image1)
    image2_fft = np.fft.fft2(image2)

    image1_fft_phaseinfo = image1_fft.copy()

    image1_fft_phaseinfo[np.abs(image1_fft) != 0] = image1_fft_phaseinfo[np.abs(image1_fft) != 0] / \
        np.abs(image1_fft)[np.abs(image1_fft) != 0]

    plt.imshow(np.abs(np.fft.ifft2(image1_fft_phaseinfo)), cmap="gray")
    plt.show()

    plt.imshow(np.log(np.abs(np.fft.fftshift(image1_fft))+1) ** intensity_factor, cmap="gray")
    plt.show()

    plt.imshow(np.log(np.abs(np.fft.fftshift(image2_fft)) + 1) ** intensity_factor, cmap="gray")
    plt.show()


if __name__ == "__main__":

    file1_path = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lena_gray_512.tif'
    file2_path = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\woman_darkhair.tif'
    inverse_fourier(file1_path, file2_path, intensity_factor=1)
