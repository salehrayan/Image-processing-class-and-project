import cv2
import math
import numpy as np
from scipy import signal
import scipy
from tqdm import tqdm
import matplotlib.pyplot as plt


np.random.seed(42)

def noise_remove(file_path, intensity_factor, std, blurring_kernel_dim, MF_dim , Mean_F_dim):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)


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
    kernel_blur = np.ones((blurring_kernel_dim, blurring_kernel_dim)) / (blurring_kernel_dim**2)
    kernel_average = np.ones((Mean_F_dim, Mean_F_dim))/ (Mean_F_dim**2)

    image_blur = signal.correlate2d(image, kernel_blur, boundary="symm")
    noise = std*np.random.randn(image_blur.shape[0], image_blur.shape[1])
    image_blur_noise = image_blur + noise

    snr = np.sum(image**2)/np.sum(np.abs(noise[blurring_kernel_dim-1:noise.shape[0]-(blurring_kernel_dim-2),
                               blurring_kernel_dim-1:noise.shape[1]-(blurring_kernel_dim-2)])**2)
    print(snr)

    kernel_blur_fft = np.fft.fft2(kernel_blur, s=(image_blur_noise.shape[0], image_blur_noise.shape[1]))
    image_blur_noise_fft = np.fft.fft2(image_blur_noise, s=(image_blur_noise.shape[0], image_blur_noise.shape[1]))


    image_laplacian = signal.correlate2d(image_blur_noise, kernel_laplacian, boundary='symm')
    # image_section = image_blur_noise[884:946, 418:872].copy()
    # std_estimate = np.std(image_section.reshape(-1))
    # print(std_estimate)

    rec_image2 = signal.correlate2d(image_blur_noise, kernel_average, boundary='symm')

    rec_image_k1 = np.abs(
        np.fft.ifft2((((np.abs(kernel_blur_fft) ** 2) / (np.abs(kernel_blur_fft) ** 2 + 1)) / (kernel_blur_fft+0.01)) *
                     image_blur_noise_fft))
    rec_image_k1 = (rec_image_k1 - np.min(rec_image_k1))/(np.max(rec_image_k1) - np.min(rec_image_k1)) *255

    rec_image_kpoint1 = np.abs(
        np.fft.ifft2((((np.abs(kernel_blur_fft) ** 2) / (np.abs(kernel_blur_fft) ** 2 + 0.1)) / (kernel_blur_fft+0.01)) *
                     image_blur_noise_fft))
    rec_image_kpoint1 = (rec_image_kpoint1 - np.min(rec_image_kpoint1)) / (np.max(rec_image_kpoint1) - np.min(rec_image_kpoint1)) * 255

    rec_image_kpoint5 = np.abs(
        np.fft.ifft2((((np.abs(kernel_blur_fft) ** 2) / (np.abs(kernel_blur_fft) ** 2 + 0.5)) / (kernel_blur_fft+0.01)) *
                     image_blur_noise_fft))
    rec_image_kpoint5 = (rec_image_kpoint5 - np.min(rec_image_kpoint5)) / (
                np.max(rec_image_kpoint5) - np.min(rec_image_kpoint5)) * 255

    rec_image_k10 = np.abs(
        np.fft.ifft2((((np.abs(kernel_blur_fft) ** 2) / (np.abs(kernel_blur_fft) ** 2 + 10)) / (kernel_blur_fft+0.01)) *
                     image_blur_noise_fft))
    rec_image_k10 = (rec_image_k10 - np.min(rec_image_k10)) / (
            np.max(rec_image_k10) - np.min(rec_image_k10)) * 255

    image_blur_noise_padded = np.pad(image_blur_noise, ((MF_dim-2, MF_dim-2), (MF_dim-2, MF_dim-2)), mode="symmetric")
    rec_image = image_blur_noise_padded.copy()
    rec_image3 = image_blur_noise_padded.copy()

    for row in tqdm(range(MF_dim-2,image_blur_noise.shape[0]+(MF_dim-2))):
        for col in range(MF_dim-2, image_blur_noise.shape[1]+(MF_dim-2)):

            temp = image_blur_noise_padded[row-(MF_dim-3):row+(MF_dim-1), col-(MF_dim-3):col+(MF_dim-1)]
            rec_image[row, col] = np.median(temp)

            '''Wiener Filter'''
            mu = np.mean(temp)
            sigma2 = np.var(temp)
            rec_image3[row, col] = mu + ((sigma2 - std**2)/(sigma2 + 0.01))*(image_blur_noise_padded[row, col]-mu)

    plt.figure(figsize=(8, 10))

    ax1 = plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Original image', fontname='Times New Roman', fontweight="bold")

    ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(image_blur_noise, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Degraded image', fontname='Times New Roman', fontweight="bold")

    ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Median filtered, dim={MF_dim}', fontname='Times New Roman', fontweight="bold")

    ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image2, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Mean filtered, dim={Mean_F_dim}', fontname='Times New Roman', fontweight="bold")

    ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image3, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Wiener filtered, dim={MF_dim}', fontname='Times New Roman', fontweight="bold")

    ax6 = plt.subplot(3, 2, 6, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image_k1+np.abs(np.mean(rec_image_k1)-np.mean(rec_image2)), cmap='gray', vmax=255, vmin=0)
    plt.title(f'Full Wiener filtered, K=1', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()

    plt.figure(figsize=(4, 10))

    ax7 = plt.subplot(3, 1, 1, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image_kpoint1+np.abs(np.mean(rec_image_kpoint1) - np.mean(rec_image2)), cmap='gray', vmax=255, vmin=0)
    plt.title(f'Full Wiener filtered, K=0.1', fontname='Times New Roman', fontweight="bold")

    ax8 = plt.subplot(3, 1, 2, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image_kpoint5 + np.abs(np.mean(rec_image_kpoint5) - np.mean(rec_image2)), cmap='gray', vmax=255,
               vmin=0)
    plt.title(f'Full Wiener filtered, K=0.5', fontname='Times New Roman', fontweight="bold")

    ax9 = plt.subplot(3, 1, 3, sharex=ax1, sharey=ax1)
    plt.imshow(rec_image_k10 + np.abs(np.mean(rec_image_k10) - np.mean(rec_image2)), cmap='gray', vmax=255,
               vmin=0)
    plt.title(f'Full Wiener filtered, K=10', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()

    plt.show()



if __name__ == '__main__':
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.02.tiff'
    noise_remove(file_path, intensity_factor=1, std=40, blurring_kernel_dim=4,
                 MF_dim=4, Mean_F_dim=4)
