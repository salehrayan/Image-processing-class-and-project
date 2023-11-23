from math import floor
import math
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
import numpy as np



def u(x,a = -0.5):

    pos_x = abs(x)
    if -1 <= abs(x) <= 1:
        return ((a+2)*(pos_x**3)) - ((a+3)*(pos_x**2)) + 1
    elif 1 < abs(x) < 2 or -2 < x < -1:
        return ((a * (pos_x**3)) - (5*a*(pos_x**2)) + (8 * a * pos_x) - 4*a)
    else:
        return 0

def bicubic_interpolation(img, factor, a):

    nrows = floor(img.shape[0] * factor)
    ncols = floor(img.shape[1] * factor)

    output = np.zeros((nrows, ncols), np.uint8)

    for i in tqdm(range(nrows)):
        for j in range(ncols):
            yo = i / factor
            xo = j / factor

            y_final = floor(yo)
            x_final = floor(xo)

            w = yo - y_final
            v = xo - x_final

            out = 0
            for n in range(-1, 3):
                for m in range(-1, 3):
                    if ((y_final + n < 0) or (y_final + n >= img.shape[0]) or (x_final + m < 0) or (x_final + m >= img.shape[1])):
                        continue

                    out += (img[y_final+n, x_final+m] * (u(w - n, a) * u(v - m, a)))


            output[i, j] = min(max(out, 0), 255)

    return output


def show_upscaled_images(file_path: str, factor, a = -0.5):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    height, width = image.shape
    new_height = math.floor(factor * height)
    new_width = math.floor(factor * width)

    upscaled_image_n = np.zeros((math.floor(height * factor), math.floor(width * factor)), dtype=np.uint8)
    upscaled_image_bil = np.zeros((math.floor(height * factor), math.floor(width * factor)), dtype=np.uint8)


    for i in tqdm(range(new_height-1)):
        for j in range(new_width-1):

            x = i / factor
            y = j / factor

            xo = floor(x)
            yo = floor(y)

            pixel_value = image[xo, yo]
            upscaled_image_n[i:i+math.ceil(factor), j:j+math.ceil(factor)] = pixel_value


    for i in tqdm(range(new_height)):
        for j in range(new_width):
            xo = j / factor
            yo = i / factor

            x_1 = math.floor(xo)
            x1 = min(x_1 + 1, width - 1)
            y_1 = math.floor(yo)
            y1 = min(y_1 + 1, height - 1)

            dx = xo - x_1
            dy = yo - y_1

            interpolated_value = (1 - dx) * (1 - dy) * image[y_1, x_1] + dx * (1 - dy) * image[y_1, x1] + (1 - dx) * dy * image[y1, x_1] + dx * dy * image[y1, x1]

            upscaled_image_bil[i, j] = interpolated_value




    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(8, 9), sharex='all', sharey='all')


    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    upscaled_image_bic = bicubic_interpolation(image, factor, a)
    ax[0,0].imshow(image, cmap='gray', vmin=0, vmax=255)
    ax[0,0].set_title('Original Image', fontname='Times New Roman', fontweight="bold")
    ax[0,1].imshow(upscaled_image_n, cmap='gray', vmin=0, vmax=255)
    ax[0,1].set_title(f'Upscaled Image, nearest neighbor\n Factor = {factor}', fontname='Times New Roman', fontweight="bold")
    ax[1,0].imshow(upscaled_image_bil, cmap='gray', vmin=0, vmax=255)
    ax[1,0].set_title(f'Upscaled Image, Bi-linear\n Factor = {factor}', fontname='Times New Roman', fontweight="bold")
    ax[1,1].imshow(upscaled_image_bic, cmap='gray', vmin=0, vmax=255)
    ax[1,1].set_title(f'Upscaled Image, Bi-cubic\n Factor = {factor}, a = {a}', fontname='Times New Roman', fontweight="bold")
    ax[2,0].imshow(resized_image, cmap='gray', vmin=0, vmax=255)
    ax[2, 0].set_title(f'Upscaled Image, Bi-cubic Open-CV implementation', fontname='Times New Roman', fontweight="bold")

    fig.delaxes(ax[2,1])
    plt.tight_layout()
    # plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9, wspace=0, hspace=0.2)
    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = 'standard_test_images/cameraman.tif'

    show_upscaled_images(file_path, 2, a= -0.5)
