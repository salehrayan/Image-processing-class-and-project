import cv2
import numpy as np
import scipy
from math import floor
import math
from tqdm import tqdm
import matplotlib.pyplot as plt


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def halfpixel_shift(file1_path):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    upscaled_image_n = np.zeros((height * 2, width * 2))
    half_pixeled = np.zeros((height * 2, width * 2 + 1))

    for i in tqdm(range(height * 2)):
        for j in range(width * 2):
            x = i / 2
            y = j / 2

            xo = floor(x)
            yo = floor(y)

            pixel_value = image[xo,   yo]
            upscaled_image_n[i:i + math.ceil(2), j:j + math.ceil(2)] = pixel_value


    for i in tqdm(range(height * 2)):
        half_pixeled[i, i % 2:width * 2 + (i % 2)] = upscaled_image_n[i]

    plt.figure(figsize=(17, 7))
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")
    plt.subplot(1, 3, 2)
    plt.imshow(upscaled_image_n, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Up-scaled image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(1, 3, 3)
    plt.imshow(half_pixeled, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Every other row shifted', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lake.tif'
    halfpixel_shift(file_path)
