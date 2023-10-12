import cv2
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def rotate_image(file_path, angle, b=-0.5):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    def u(x,a=-0.5):
        pos_x = abs(x)
        if -1 <= abs(x) <= 1:
            return ((a+2)*(pos_x**3)) - ((a+3)*(pos_x**2)) + 1
        elif 1 < abs(x) < 2 or -2 < x < -1:
            return (a * (pos_x**3)) - (5*a*(pos_x**2)) + (8 * a * pos_x) - 4*a
        else:
            return 0

    "OPEN CV"
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), -1*angle, 1)
    rotated_image_cv = cv2.warpAffine(image, rotation_matrix, (width, height))
    "================"

    angle_radians = angle*np.pi/180

    alpha = np.cos(angle_radians)
    beta = np.sin(angle_radians)

    aff_matrix = np.array([[alpha, -1 * beta],
                           [beta, alpha]])
    # aff_matrix_inverse = np.linalg.inv(aff_matrix)

    aff_matrix_inverse = np.array([[alpha,  beta],
                           [-1 * beta, alpha]])

    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    translation_matrix = np.array([[1,0,700/2 - image.shape[1]],
                                   [0,1, 700/2 - image.shape[0]],
                                   [0, 0, 1]])

    translation_inverse_matrix = np.linalg.inv(translation_matrix)



    rotated_image_nearest = np.zeros((height, width), dtype=np.uint8)
    rotated_image_bilinear = np.zeros((height, width), dtype=np.uint8)
    rotated_image_bicubic = np.zeros((height, width), dtype=np.uint8)
    rotated_image_cv_all_encompass = np.zeros((700,700), dtype=np.uint8)
    output_coordinates = np.empty((2, 1), dtype=np.uint16)
    output_coordinates_new = np.empty((3, 1), dtype=np.uint16)

    for y in tqdm(range(image.shape[0])):
        for x in range(image.shape[1]):
            """extract original coordinates and ignore coordinates out of bound"""
            output_coordinates[0, 0] = int(x)
            output_coordinates[1, 0] = int(y)
            original_coordinates = np.matmul(aff_matrix_inverse, output_coordinates)
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

                    out += (image[y_final + n, x_final + m] * (u(w - n, b) * u(v - m, b)))

            rotated_image_bicubic[y, x] = min(max(out, 0), 255)


    # for y in tqdm(range(rotated_image_cv_all_encompass.shape[0])):
    #     for x in range(rotated_image_cv_all_encompass.shape[1]):
    #         """extract original coordinates and ignore coordinates out of bound"""
    #         output_coordinates_new[0, 0] = int(x)
    #         output_coordinates_new[1, 0] = int(y)
    #         output_coordinates_new[2, 0] = 1
    #
    #         original_coordinates = np.matmul(translation_inverse_matrix, np.matmul(rotation_matrix, output_coordinates_new))
    #         if (original_coordinates[0, 0] < 0) or (original_coordinates[0, 0] > image.shape[1]-1) or (original_coordinates[1, 0] < 0) or (original_coordinates[1, 0] > image.shape[0] - 1):
    #             continue
    #
    #         xo = original_coordinates[0,0]
    #         yo = original_coordinates[1,0]
    #
    #         y_final = math.floor(yo)
    #         x_final = math.floor(xo)
    #
    #         w = yo - y_final
    #         v = xo - x_final
    #
    #         out = 0
    #         for n in range(-1, 3):
    #             for m in range(-1, 3):
    #                 if ((y_final + n < 0) or (y_final + n >= image.shape[0]) or (x_final + m < 0) or (
    #                         x_final + m >= image.shape[1])):
    #                     continue
    #
    #                 out += (image[y_final + n, x_final + m] * (u(w - n, b) * u(v - m, b)))
    #
    #         rotated_image_cv_all_encompass[y, x] = min(max(out, 0), 255)


    plt.figure(figsize=(7,10))
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
    # ax6 = plt.subplot(326)
    # ax6.imshow(rotated_image_cv_all_encompass, cmap='gray', vmin=0, vmax=255)
    # ax6.set_title(f'Manual Affine Matrix Wide\nBi-cubic Interpolation\nθ = {angle}°', fontname='Times New Roman',
    #               fontweight="bold")



    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = 'standard_test_images/cameraman.tif'
    rotate_image(file_path, 18)