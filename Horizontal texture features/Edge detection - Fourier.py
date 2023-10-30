import cv2
import math
import numpy as np
from scipy import signal
from tqdm import tqdm
import matplotlib.pyplot as plt


def horizontal_textures(file_path, intensity_factor, h_lower_lim, h_higher_lim, v_lower_lim, v_higher_lim):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    fourier = np.fft.fft2(image)
    fourier_shifted = np.log(np.abs(np.fft.fftshift(fourier))) ** intensity_factor
    fourier_filtered = np.zeros(fourier.shape, dtype=np.complex128)

    # fourier_filtered[int(v_lower_lim*height/2):int(v_higher_lim*height/2),
    # int(h_lower_lim*width/2):int(h_higher_lim*width/2)] = 4 * fourier[int(v_lower_lim*height/2):int(v_higher_lim*height/2),
    # int(h_lower_lim*width/2):int(h_higher_lim*width/2)]
    fourier_filtered[813 :1024, 0: 20] = 4 *fourier[813 :1024, 0: 20]
    # fourier_filtered[-horizontal_edge_factor:, width//16:width//2] = fourier[-horizontal_edge_factor:, width//16:width//2]

    # if vertical_edge_factor != 0:
    #     fourier_filtered[:, 0:vertical_edge_factor] = fourier[:, 0:vertical_edge_factor]
    #     fourier_filtered[:, -vertical_edge_factor:] = fourier[:, -vertical_edge_factor:]

    # fourier_filtered[0,0] = 0

    temp2 = fourier_filtered.copy()
    fourier_filtered_inverse = np.abs(np.fft.ifft2(fourier_filtered))

    plt.figure(figsize=(8, 9))

    ax1 = plt.subplot(2, 2, 1)
    plt.imshow(image, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")
    #
    ax2 = plt.subplot(2, 2, 2, sharex=ax1, sharey=ax1)
    plt.imshow(np.log(np.abs(fourier)) ** intensity_factor, cmap='gray', vmax=255, vmin=0)
    plt.title(f'FFT of the image', fontname='Times New Roman', fontweight="bold")
    #
    ax3 = plt.subplot(2, 2, 3, sharex=ax1, sharey=ax1)
    plt.imshow(fourier_shifted, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Shifted FFT', fontname='Times New Roman', fontweight="bold")
    #
    ax4 = plt.subplot(2, 2, 4, sharex=ax1, sharey=ax1)
    plt.imshow(fourier_filtered_inverse, cmap='gray', vmax=255, vmin=0)
    plt.title(f'Inverse FFT of filtered fourier domain',
              fontname='Times New Roman', fontweight="bold")
    plt.tight_layout()

    plt.figure(figsize=(6,7))
    plt.imshow(np.log(np.abs(temp2)+0.01) ** intensity_factor,  cmap='gray', vmax=255, vmin=0)
    plt.title('Filtered FFT')

    plt.tight_layout()
    plt.show()




if __name__ == '__main__':
    file_path = r'textures\1.4.03.tiff'
    horizontal_textures(file_path, intensity_factor=2, h_lower_lim=0.025, h_higher_lim=0.6, v_lower_lim=0,
                        v_higher_lim=0.1)