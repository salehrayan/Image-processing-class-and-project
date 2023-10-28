import cv2
import math
import numpy as np
from scipy import signal
from tqdm import tqdm
import matplotlib.pyplot as plt


image = cv2.imread(r'textures/1.3.12.tiff', cv2.IMREAD_GRAYSCALE)

kernel_horizontal = np.array([[0, 0, 0],
                   [2, -4, 2],
                   [0, 0, 0]]) / 8

kernel_vertical = np.array([[0, 2, 0],
                   [0, -4, 0],
                   [0, 2, 0]]) / 8

kernel_diagonal = np.array([[1, 0, 1],
                   [0, -4, 0],
                   [1, 0, 1]]) / 8
kernel_laplacian = np.array([[1, 1, 1],
                   [1, -8, 1],
                   [1, 1, 1]]) / 16
kernel_average = np.array([[1, 1],
                           [1, 1]]) / 4

output_kernel_horizontal = signal.correlate2d(image, kernel_horizontal)
output_kernel_diagonal = signal.correlate2d(image, kernel_diagonal)
output_kernel_vertical = signal.correlate2d(image, kernel_vertical)
output_kernel_laplacian = signal.correlate2d(image, kernel_laplacian)

difference = output_kernel_laplacian - output_kernel_vertical

difference_averaged = signal.correlate2d(difference, kernel_average)


plt.figure(figsize=(9, 10))
ax1 = plt.subplot(3, 2, 1)
plt.imshow(image, cmap='gray')
plt.title(f'Image', fontname='Times New Roman', fontweight="bold")

ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
plt.imshow(output_kernel_horizontal, cmap='gray')
plt.title(f'Output of horizontal kernel', fontname='Times New Roman', fontweight="bold")

ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
plt.imshow(output_kernel_vertical, cmap='gray')
plt.title(f'Output of vertical kernel', fontname='Times New Roman', fontweight="bold")

ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
plt.imshow(output_kernel_laplacian, cmap='gray')
plt.title(f'Output of Laplacian kernel', fontname='Times New Roman', fontweight="bold")

ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
plt.imshow(difference, cmap='gray')
plt.title(f'Laplacian minus vertical', fontname='Times New Roman', fontweight="bold")

ax6 = plt.subplot(3, 2, 6, sharex=ax1, sharey=ax1)
plt.imshow(difference_averaged, cmap='gray')


plt.tight_layout()
plt.show()
