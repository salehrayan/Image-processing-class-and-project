import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

np.random.seed(42)


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def motion_blur(file1_path):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    image_fft = np.fft.fft2(image)

    T = 1  # exposure
    a = 0.1  # vertical motion
    b = 0.1  # horizontal motion

    H = np.zeros((height + 1, width + 1), dtype=np.complex128)  # +1 to avoid zero division
    # Fill matrix H
    for u in range(1, height + 1):
        for v in range(1, width + 1):
            s = np.pi * (u * a + v * b)
            H[u, v] = (T / s) * np.sin(s) * np.exp(-1j * s)


    # index slicing to remove the +1 that we have added before for avoiding zero division
    H = H[1:, 1:]


    plt.figure(figsize=(17, 9))
    # ax_im = plt.subplot(1, 3, 1)
    plt.imshow(np.real(np.fft.ifft2(np.fft.ifftshift((np.fft.fftshift(image_fft) * np.fft.fftshift(H))))), cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")



    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = r'book.jpg'
    motion_blur(file_path)
