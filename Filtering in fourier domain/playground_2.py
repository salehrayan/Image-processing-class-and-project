import cv2
import math
import numpy as np
from scipy import signal
from tqdm import tqdm
import matplotlib.pyplot as plt


def fftshift_in_time(x):
    temp = x.copy()
    for row in range(temp.shape[0]):
        for col in range(temp.shape[1]):
            temp[row, col] = (1 - ((row + col) % 2)) * temp[row, col]
    return temp


kernel_laplacian = np.array([[1, 0, 1],
                             [0, 4, 0],
                             [1, 0, 1]])
image = cv2.imread(r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lena_gray_512.tif',
                   cv2.IMREAD_GRAYSCALE)

image_fft = np.fft.fft2(fftshift_in_time(image))
image_fft2 = np.fft.fft2(fftshift_in_time(image), s=(image.shape[0]*2, image.shape[1]*2))
image2_inversefft = np.fft.ifft2(np.fft.ifftshift(image_fft2))
plt.imshow(np.real(image2_inversefft), cmap='gray', vmin=0, vmax=255)

plt.show()
