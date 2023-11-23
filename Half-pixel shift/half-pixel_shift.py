import cv2
import numpy as np
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def halfpixel_shift(file1_path):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)

    # plt.subplot(3, 4, 1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")
    #
    # plt.subplot(3, 4, 2)
    # plt.imshow(image2, cmap="gray", vmin=0, vmax=255)
    # plt.title(f'Image 2', fontname='Times New Roman', fontweight="bold")
    #
    # plt.subplot(3, 4, 3)
    # plt.imshow(np.log(np.abs(np.fft.fftshift(image1_fft)) + 1) ** intensity_factor, cmap="gray", vmin=0, vmax=255)
    # plt.title(f'Image 1 Magnitude spectrum', fontname='Times New Roman', fontweight="bold")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lake.tif'
    halfpixel_shift(file_path)
