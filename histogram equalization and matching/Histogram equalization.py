import cv2
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def histogram_equalize(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_equalized = image.copy()
    height, width = image.shape

    coefficient = 255/(height*width)

    values, bins = np.histogram(image, bins=256)

    for pixel_value in range(256):
        image_equalized[image == pixel_value] = max(int(coefficient * np.sum(values[0:pixel_value+1])), 0)

    plt.figure(figsize=(13, 9))
    plt.subplot(2, 2, 1)
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title('Original image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 2, 2, sharex=plt.gca(), sharey=plt.gca())
    plt.imshow(image_equalized, cmap='gray', vmin=0, vmax=255)
    plt.title('Equalized image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 2, 3)
    plt.hist(image.reshape(-1), bins=256)
    plt.title('Histogram of the original image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 2, 4, sharex=plt.gca(), sharey=plt.gca())
    plt.hist(image_equalized.reshape(-1), bins=256)
    plt.title('Histogram of the equalized image', fontname='Times New Roman', fontweight="bold")
    plt.tight_layout()

    plt.figure(figsize=(5, 5))
    plt.plot(range(len(values)), np.floor(coefficient * np.cumsum(values)), color='black')
    plt.title('Transformation function', fontname='Times New Roman', fontweight="bold")
    plt.show()


if __name__ == "__main__":
    file_path = r'C:\Users\ASUS\Desktop\Image processing\rotate and resize\standard_test_images\cameraman.tif'
    # file_path = r'Untitled.png'
    histogram_equalize(file_path)