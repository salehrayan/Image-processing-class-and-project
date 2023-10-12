import math
import matplotlib.pyplot as plt
import cv2
from tqdm.auto import tqdm
import numpy as np


def show_upscaled_images(file_path: str, factor, a = -0.5):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Get the original image dimensions
    height, width = image.shape
    new_height = math.floor(factor * height)
    new_width = math.floor(factor * width)

    # Create an empty image with double the dimensions
    upscaled_image_n = np.zeros((math.floor(height * factor), math.floor(width * factor)), dtype=np.uint8)
    upscaled_image_bil = np.zeros((math.floor(height * factor), math.floor(width * factor)), dtype=np.uint8)
    upscaled_image_bic = np.zeros((math.floor(height * factor), math.floor(width * factor)), dtype=np.uint8)


    def u(s,a):
        if (abs(s) >=0) & (abs(s) <=1):
            return (a+2)*(abs(s)**3)-(a+3)*(abs(s)**2)+1
        elif (abs(s) > 1) & (abs(s) <= 2):
            return a*(abs(s)**3)-(5*a)*(abs(s)**2)+(8*a)*abs(s)-4*a
        return 0

    for i in tqdm(range(height)):
        for j in range(width):
            pixel_value = image[i, j]
            upscaled_image_n[math.floor(i * factor), math.floor(j * factor)] = pixel_value
            upscaled_image_n[math.floor(i * factor), min(math.floor(j * factor + 1), new_width -1)] = pixel_value
            upscaled_image_n[min(math.floor(i * factor + 1), new_height-1), math.floor(j * factor)] = pixel_value
            upscaled_image_n[min(math.floor(i * factor + 1), new_height-1), min(math.floor(j * factor + 1), new_width -1)] = pixel_value

    for i in tqdm(range(new_height)):
        for j in range(new_width):
            # Calculate the corresponding position in the original image
            x = j / factor
            y = i / factor

            # Find the four nearest neighboring pixels
            x_1 = math.floor(x)
            x1 = min(x_1 + 1, width - 1)
            y_1 = math.floor(y)
            y1 = min(y_1 + 1, height - 1)


            dx = x - x_1
            dy = y - y_1


            interpolated_value = (1 - dx) * (1 - dy) * image[y_1, x_1] + dx * (1 - dy) * image[y_1, x1] + (1 - dx) * dy * image[y1, x_1] + dx * dy * image[y1, x1]

            upscaled_image_bil[i, j] = interpolated_value


    for i in tqdm(range(new_height)):
        for j in range(new_width):

            x = j / factor
            y = i / factor

            x_1 = math.floor(x)
            y_1 = math.floor(y)
            x_2 = max(x_1 - 1, 0)
            y_2 = max(y_1 - 1, 0)
            x_2_real = x_1-1
            y_2_real = y_1-1

            x1 = min(x_1 + 1, width - 1)
            y1 = min(y_1 + 1, height - 1)
            x1_real = x_1 + 1
            y1_real = y_1 + 1
            x2 = min(x_1 + 2, width - 1)
            y2 = min(y_1 + 2, height - 1)
            x2_real = x_1 + 2
            y2_real = y_1 + 2

            mat1 = np.array([[u(x-x_2_real,a), u(x-x_1,a), u(x-x1_real,a), u(x-x2_real,a)]])
            mat2 = np.array([[image[y_2, x_2], image[y_1, x_2], image[y1, x_2], image[y2, x_2]],
                             [image[y_2, x_1], image[y_1, x_1], image[y1, x_1], image[y2, x_1]],
                             [image[y_2, x1], image[y_1, x1], image[y1, x1], image[y2, x1]],
                             [image[y_2, x2], image[y_1, x2], image[y1, x2], image[y2, x2]]])
            mat3 = np.array([[u(y-y_2_real,a)],
                             [u(y-y_1,a)],
                             [u(y-y1_real,a)],
                             [u(y-y2_real,a)]])

            b = np.matmul(np.matmul(mat1,mat2), mat3)

            # if (i == 1019) and (j == 89):
            #     raise Exception

            upscaled_image_bic[i, j] = max(np.matmul(np.matmul(mat1,mat2), mat3), 0)



    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(10, 10), sharex=True, sharey=True) # type:axes.Axes


    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    ax[0,0].imshow(image, cmap='gray', vmin=0, vmax=255)
    ax[0,0].set_title('Original Image')
    ax[0,1].imshow(upscaled_image_n, cmap='gray', vmin=0, vmax=255)
    ax[0,1].set_title(f'Upscaled Image, nearest neighbor\n Factor = {factor}')
    ax[1,0].imshow(upscaled_image_bil, cmap='gray', vmin=0, vmax=255)
    ax[1,0].set_title(f'Upscaled Image, Bi-linear\n Factor = {factor}')
    ax[1,1].imshow(upscaled_image_bic, cmap='gray', vmin=0, vmax=255)
    ax[1,1].set_title(f'Upscaled Image, Bi-cubic\n Factor = {factor}, a = {a}')
    ax[2,0].imshow(resized_image, cmap='gray', vmin=0, vmax=255)
    ax[2, 0].set_title(f'Upscaled Image, Bi-cubic Open-CV implementation')

    fig.delaxes(ax[2,1])
    plt.tight_layout()
    # plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9, wspace=0, hspace=0.2)
    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = 'standard_test_images/woman_blonde.tif'

    show_upscaled_images(file_path, 2)

