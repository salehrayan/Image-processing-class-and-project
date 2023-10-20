import cv2
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def histogram_match(reference_image_path, target_image_path):
    image_reference = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
    image_target = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    image_matched = image_target.copy()
    height_ref, width_ref = image_reference.shape
    height_target, width_target = image_target.shape

    coefficient_ref = 255/(height_ref * width_ref)
    coefficient_target = 255/(height_target * width_target)

    values_ref, _ = np.histogram(image_reference, bins=256)
    values_target, _ = np.histogram(image_target, bins=256)
    ref_trans_function = np.floor(coefficient_ref * np.cumsum(values_ref))
    target_trans_function = np.floor(coefficient_target * np.cumsum(values_target))

    for pixel_value in range(256):
        if np.argwhere(ref_trans_function == target_trans_function[pixel_value]).shape != (0,1):
            image_matched[image_target == pixel_value] = np.argwhere(ref_trans_function == target_trans_function[pixel_value])[
                int(len(np.argwhere(ref_trans_function == target_trans_function[pixel_value]))/2)]
        else:
            image_matched[image_target == pixel_value] = np.abs(ref_trans_function - target_trans_function[pixel_value]).argmin(keepdims=True)[
                int(len(np.abs(ref_trans_function - target_trans_function[pixel_value]).argmin(keepdims=True)) / 2)]

    plt.figure(figsize=(15, 9))
    plt.subplot(2, 3, 1)
    plt.imshow(image_reference, cmap='gray', vmin=0, vmax=255)
    plt.title('Reference image', fontname='Times New Roman', fontweight="bold")
    #
    plt.subplot(2, 3, 2)
    plt.imshow(image_target, cmap='gray', vmin=0, vmax=255)
    plt.title('Target Image image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 3)
    plt.imshow(image_matched, cmap='gray', vmin=0, vmax=255)
    plt.title('Target histogram matched image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 4)
    plt.hist(image_reference.reshape(-1), bins=256)
    plt.title('Histogram of the reference image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 5)
    plt.hist(image_target.reshape(-1), bins=256)
    plt.title('Histogram of the target image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 6)
    plt.hist(image_matched.reshape(-1), bins=256)
    plt.title('Histogram of the matched target image', fontname='Times New Roman', fontweight="bold")
    plt.tight_layout()

    plt.figure(figsize=(5, 5))
    plt.plot(range(len(values_ref)), ref_trans_function, color='blue', label='Reference transfer function')
    plt.plot(range(len(values_target)), target_trans_function, color='red', label='Target transfer function')
    plt.title('Transformation function', fontname='Times New Roman', fontweight="bold")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    reference_path = r'C:\Users\ASUS\Desktop\Image processing\rotate and resize\standard_test_images\cameraman.tif'
    target_path = r'C:\Users\ASUS\Desktop\Image processing\rotate and resize\standard_test_images\lena_gray_512.tif'
    # file_path = r'Untitled.png'
    histogram_match(reference_path, target_path)