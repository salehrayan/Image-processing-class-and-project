import cv2
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

shape = 512
image = np.zeros((shape, shape), dtype=np.uint8)
image[:,:] = 128
angle = 15

middle = math.floor(shape / 2)
t_c_h = math.floor(shape / 3.2)
t_c_w = math.floor(shape / 20)

t_h_h = math.floor(1.6 * shape / 20)
t_h_w = math.floor(t_c_h / 1.5)

image[middle - t_c_h: middle+t_c_h, middle-t_c_w: middle+t_c_w] = 255
image[middle - t_c_h: middle - t_c_h + t_h_h, middle-t_h_w: middle+t_h_w] = 255


def u(x,a = -0.5):

    pos_x = abs(x)
    if -1 <= abs(x) <= 1:
        return ((a+2)*(pos_x**3)) - ((a+3)*(pos_x**2)) + 1
    elif 1 < abs(x) < 2 or -2 < x < -1:
        return (a * (pos_x**3)) - (5*a*(pos_x**2)) + (8 * a * pos_x) - 4*a
    else:
        return 0
a = -0.5

"OPEN CV"
height, width = image.shape[:2]
rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
rotated_image_cv = cv2.warpAffine(image, rotation_matrix, (width, height))
"================"

angle_radians = angle*np.pi/180

aff_matrix = np.array([[np.cos(angle_radians), -1 * np.sin(angle_radians)],
                       [np.sin(angle_radians), np.cos(angle_radians)]])
# aff_matrix_inverse = np.linalg.inv(aff_matrix)

aff_matrix_inverse = np.array([[np.cos(angle_radians),  np.sin(angle_radians)],
                       [-1 * np.sin(angle_radians), np.cos(angle_radians)]])

rotated_image_nearest = np.zeros((height, width), dtype=np.uint8)
rotated_image_bilinear = np.zeros((height, width), dtype=np.uint8)
rotated_image_bicubic = np.zeros((height, width), dtype=np.uint8)
output_coordinates = np.empty((2, 1), dtype=np.uint16)
for y in tqdm(range(image.shape[0])):
    for x in range(image.shape[1]):
        """extract original coordinates and ignore coordinates out of bound"""
        output_coordinates[0, 0] = int(x)
        output_coordinates[1, 0] = int(y)
        original_coordinates = np.matmul(aff_matrix, output_coordinates)
        if (original_coordinates[0, 0] < 0) or (original_coordinates[0, 0] > image.shape[1]-1) or (original_coordinates[1, 0] < 0) or (original_coordinates[1, 0] > image.shape[0] - 1):
            continue

        xo = original_coordinates[0,0]
        yo = original_coordinates[1,0]

        '''nearest neighbor interpolation'''
        rotated_image_nearest[y, x] = image[math.floor(yo), math.floor(xo)]

        '''Bi-linear interpolation'''
        x_1 = math.floor(xo)
        x1 = min(x_1 + 1, width - 1)
        y_1 = math.floor(yo)
        y1 = min(y_1 + 1, height - 1)

        dx = xo - x_1
        dy = yo - y_1

        rotated_image_bilinear[y, x] = (1 - dx) * (1 - dy) * image[y_1, x_1] + dx * (1 - dy) * image[y_1, x1] + (1 - dx) * dy * image[
            y1, x_1] + dx * dy * image[y1, x1]

        '''Bi-cubic interpolation'''

        y_final = math.floor(yo)
        x_final = math.floor(xo)

        w = yo - y_final
        v = xo - x_final

        out = 0
        for n in range(-1, 3):
            for m in range(-1, 3):
                if ((y_final + n < 0) or (y_final + n >= image.shape[0]) or (x_final + m < 0) or (
                        x_final + m >= image.shape[1])):
                    continue

                out += (image[y_final + n, x_final + m] * (u(w - n, a) * u(v - m, a)))

        rotated_image_bicubic[y, x] = min(max(out, 0), 255)


fig = plt.figure(figsize=(7,9))
ax1 = plt.subplot(321)
ax1.imshow(image, cmap='gray', vmin=0, vmax=255)
ax1.set_title('Original Image', fontname='Times New Roman', fontweight="bold")
ax2 = plt.subplot(322, sharex=ax1, sharey = ax1)
ax2.imshow(rotated_image_cv, cmap='gray', vmin=0, vmax=255)
ax2.set_title(f'Open-CV rotate, θ = {angle}°', fontname='Times New Roman', fontweight="bold")
ax3 = plt.subplot(323, sharex=ax1, sharey = ax1)
ax3.imshow(rotated_image_nearest, cmap='gray', vmin=0, vmax=255)
ax3.set_title(f'Manual Affine Matrix\nNearest Neighbor Interpolation\nθ = {angle}°', fontname='Times New Roman', fontweight="bold")
ax4 = plt.subplot(324, sharex=ax1, sharey = ax1)
ax4.imshow(rotated_image_bilinear, cmap='gray', vmin=0, vmax=255)
ax4.set_title(f'Manual Affine Matrix\nBi-linear Interpolation\nθ = {angle}°', fontname='Times New Roman', fontweight="bold")

ax5 = plt.subplot(325, sharex=ax1, sharey = ax1)
ax5.imshow(rotated_image_bicubic, cmap='gray', vmin=0, vmax=255)
ax5.set_title(f'Manual Affine Matrix\nBi-cubic Interpolation\nθ = {angle}°', fontname='Times New Roman', fontweight="bold")


plt.tight_layout()
plt.show()
