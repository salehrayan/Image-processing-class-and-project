import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

np.random.seed(42)


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def Adaptive_median_filter(file1_path, P_SandP, Smax):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape

    salt_pepper_index = np.random.uniform(0, 1, image.shape)

    salty_peppered_image = image.copy()
    salty_peppered_image[salt_pepper_index < P_SandP] = 255
    salty_peppered_image[np.bitwise_and(salt_pepper_index >= P_SandP, salt_pepper_index < 2 * P_SandP)] = 0

    image_padded = np.pad(salty_peppered_image, ((Smax // 2, Smax // 2), (Smax // 2, Smax // 2)))
    print(image_padded.shape)

    '''##### adaptive median filter'''
    for row in tqdm(np.arange(height) + Smax // 2):
        for col in np.arange(width) + Smax // 2:
            for Sxy in range(3, Smax + 1, 2):
                temp = image_padded[row - Sxy // 2:row + (Sxy // 2 + 1), col - Sxy // 2:col + (Sxy // 2 + 1)]

                if np.min(temp) < np.median(temp) < np.max(temp):
                    if np.min(temp) < image_padded[row, col] < np.max(temp):
                        break
                    else:
                        image_padded[row, col] = np.median(temp)
                else:
                    continue
                if Sxy > Smax:
                    image_padded[row, col] = np.median(temp)
    '''###########################'''

    plt.figure(figsize=(17, 9))
    ax_im = plt.subplot(1, 3, 1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(1, 3, 2, sharex=ax_im, sharey=ax_im)
    plt.imshow(salty_peppered_image, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image with salt-and-pepper noise\nPs=Pp={P_SandP}', fontname='Times New Roman', fontweight="bold")

    plt.subplot(1, 3, 3, sharex=ax_im, sharey=ax_im)
    plt.imshow(image_padded[Smax // 2:height + Smax // 2, Smax // 2:width + Smax // 2], cmap="gray", vmin=0, vmax=255)
    plt.title(f'Adaptive median filtered image\n'
              f'SNR = {10 * np.log(np.sum(image ** 2) / np.sum((image - image_padded[Smax // 2:height + Smax // 2, Smax // 2:width + Smax // 2]) ** 2)):.2f}dB'
              f'\n PSNR = {10 * np.log(np.max(image) ** 2 / np.mean((image - image_padded[Smax // 2:height + Smax // 2, Smax // 2:width + Smax // 2]) ** 2)):.2f}dB',
              fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\lena_gray_512.tif'
    Adaptive_median_filter(file_path, P_SandP=0.25, Smax=7)
