import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def inverse_fourier(file1_path, file2_path, intensity_factor, T=None):
    image1 = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)

    if T is not None:
        image2 = T
    else:
        image2 = cv2.imread(file2_path, cv2.IMREAD_GRAYSCALE)

    image1_fft = np.fft.fft2(image1)
    image2_fft = np.fft.fft2(image2)

    image1_fft_phaseinfo = image1_fft.copy()
    image2_fft_phaseinfo = image2_fft.copy()


    image1_fft_phaseinfo[np.abs(image1_fft) != 0] = image1_fft_phaseinfo[np.abs(image1_fft) != 0] / \
                                                    np.abs(image1_fft)[np.abs(image1_fft) != 0]

    image2_fft_phaseinfo[np.abs(image2_fft) != 0] = image2_fft_phaseinfo[np.abs(image2_fft) != 0] / \
                                                    np.abs(image2_fft)[np.abs(image2_fft) != 0]

    im1phase_im2spec = image1_fft_phaseinfo * np.abs(image2_fft)
    im2phase_im1spec = image2_fft_phaseinfo * np.abs(image1_fft)

    fig1 = plt.figure(figsize=(16, 10))


    plt.subplot(3, 4, 1)
    plt.imshow(image1, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 1', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 2)
    plt.imshow(image2, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 2', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 3)
    plt.imshow(np.log(np.abs(np.fft.fftshift(image1_fft)) + 1) ** intensity_factor, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 1 Magnitude spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 4)
    plt.imshow(np.log(np.abs(np.fft.fftshift(image2_fft)) + 1) ** intensity_factor, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 2 Magnitude spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 5)
    plt.imshow(minmax(np.abs(image1_fft_phaseinfo)), cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 1 Phase spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 6)
    plt.imshow(minmax(np.abs(image2_fft_phaseinfo)), cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 2 phase spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 7)
    plt.imshow(minmax(np.abs(np.fft.ifft2(np.abs(image1_fft).astype(complex)))) ** 1.5, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 1 rec. from spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 8)
    plt.imshow(minmax(np.abs(np.fft.ifft2(np.abs(image2_fft).astype(complex)))) ** 1.5, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 2 rec. from spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 9)
    plt.imshow(minmax(np.abs(np.fft.ifft2(image1_fft_phaseinfo))) * intensity_factor, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 1 rec. from phase', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 10)
    plt.imshow(minmax(np.abs(np.fft.ifft2(image2_fft_phaseinfo))) * intensity_factor, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image 2 rec. from phase.', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 11)
    plt.imshow(minmax(np.abs(np.fft.ifft2(im1phase_im2spec))), cmap="gray", vmin=0, vmax=255)
    plt.title(f'Rec. with Image 1 phase\nand Image 2 mag. spectrum', fontname='Times New Roman', fontweight="bold")

    plt.subplot(3, 4, 12)
    plt.imshow(minmax(np.abs(np.fft.ifft2(im2phase_im1spec))), cmap="gray", vmin=0, vmax=255)
    plt.title(f'Rec. with Image 2 phase\nand Image 1 mag. spectrum', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file1 = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lena_gray_512.tif'
    file2 = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lake.tif'
    'Making T'
    shape = 512
    image_T = np.zeros((512, 512), dtype=np.uint8)
    image_T[:, :] = 0

    middle = math.floor(shape / 2)
    t_c_h = math.floor(shape / 3.2)
    t_c_w = math.floor(shape / 20)
    t_h_h = math.floor(1.6 * shape / 20)
    t_h_w = math.floor(t_c_h / 1.5)

    image_T[middle - t_c_h: middle + t_c_h, middle - t_c_w: middle + t_c_w] = 255
    image_T[middle - t_c_h: middle - t_c_h + t_h_h, middle - t_h_w: middle + t_h_w] = 255

    inverse_fourier(file1, file2, intensity_factor=2.1, T=image_T)
