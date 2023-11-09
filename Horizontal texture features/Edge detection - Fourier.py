import cv2
import math
import numpy as np
from scipy import signal
from tqdm import tqdm
import matplotlib.pyplot as plt


def horizontal_textures(file_path, intensity_factor, image_selection = 0):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    fourier = np.fft.fft2(image)
    fourier_shifted = np.log(np.abs(np.fft.fftshift(fourier))+1) ** intensity_factor
    fourier_filtered = np.zeros(fourier.shape, dtype=np.complex128)
    fourier_filtered2 = np.zeros(fourier.shape, dtype=np.complex128)

    fourier_filtered[0:12, 10: 90] = 4 * fourier[0:12, 10: 90]
    fourier_filtered[4:512, 0: 10] = 4 * fourier[4:512, 0: 10]
    fourier_filtered[505:512, 20: 120] = 4 * fourier[505:512, 20: 120]
    # fourier_filtered[3:25, 3: 25] = 4 * fourier[3:25, 3: 25]
    fourier_filtered2[252:260, 259:450] = 2 * np.fft.fftshift(fourier)[252:260, 259:450]
    # fourier_filtered2[258:330, 256] = 2 * np.fft.fftshift(fourier)[258:330, 256]


    fourier_filtered_inverse = np.abs(np.fft.ifft2(fourier_filtered))
    fourier_filtered_inverse2 = np.abs(np.fft.ifft2(np.fft.ifftshift(fourier_filtered2)))

    plt.figure(figsize=(8, 9))

    ax1 = plt.subplot(2, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")
    #
    ax2 = plt.subplot(2, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(np.log(np.abs(fourier)+1) ** intensity_factor, cmap='gray')
    plt.title(f'FFT of the image', fontname='Times New Roman', fontweight="bold")
    #
    ax3 = plt.subplot(2, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(fourier_shifted, cmap='gray')
    plt.title(f'Shifted FFT', fontname='Times New Roman', fontweight="bold")
    #
    ax4 = plt.subplot(2, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(fourier_filtered_inverse2, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Inverse FFT of filtered fourier domain',
              fontname='Times New Roman', fontweight="bold")
    plt.tight_layout()

    plt.figure(figsize=(6,7))
    plt.imshow(np.log(np.abs(fourier_filtered2)+1) ** intensity_factor,  cmap='gray', vmax=255, vmin=0)
    plt.title('Filtered FFT')

    plt.tight_layout()
    plt.show()




if __name__ == '__main__':
    file_path = r'textures\1.2.12.tiff'
    horizontal_textures(file_path, intensity_factor=1)