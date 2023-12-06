import cv2
import numpy as np
import matplotlib.pyplot as plt


def minmax(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array)) * 255


def periodic_noise_remove(file1_path, n, D0):
    image = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    image_fft = np.fft.fft2(image)

    x_temp = np.linspace(-height / 2, height / 2, height)
    y_temp = np.linspace(-width / 2, width / 2, width)
    Y, X = np.meshgrid(y_temp, x_temp)

    notchpair1_x = 404 - height/2
    notchpair1_y = 766 - width/2
    notchpair2_x = 504 - height/2
    notchpair2_y = 667 - width/2

    D1 = np.hypot(X - notchpair1_x, Y - notchpair1_y)
    D_1 = np.hypot(X + notchpair1_x, Y + notchpair1_y)
    D2 = np.hypot(X - notchpair2_x, Y - notchpair2_y)
    D_2 = np.hypot(X + notchpair2_x, Y + notchpair2_y)

    NRfilter = (1/(1+(D0/D1)**(2*n)))*(1/(1+(D0/D_1)**(2*n)))*(1/(1+(D0/D2)**(2*n)))*(1/(1+(D0/D_2)**(2*n)))

    plt.figure(figsize=(17, 9))
    ax_im = plt.subplot(2, 3, 1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.title(f'Image', fontname='Times New Roman', fontweight="bold")
    ax_fft = plt.subplot(2, 3, 2)
    plt.imshow(np.log(np.abs(np.fft.fftshift(image_fft))+1), cmap="gray")
    plt.title(f'FFT of image', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 3, sharex=ax_fft, sharey=ax_fft)
    plt.imshow(np.log(np.abs(np.fft.fftshift(image_fft))+1)**3, cmap="gray")
    plt.title(f'FFT Contrast enhanced', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 4, sharex=ax_fft, sharey=ax_fft)
    plt.imshow(np.log(np.abs(np.fft.fftshift(image_fft) * NRfilter) + 1), cmap="gray")
    plt.title(f'Noise frequencies filtered\nD0 = {D0}, order = {n}', fontname='Times New Roman', fontweight="bold")

    plt.subplot(2, 3, 5, sharex=ax_im, sharey=ax_im)
    plt.imshow(np.real(np.fft.ifft2(np.fft.ifftshift(np.fft.fftshift(image_fft) * NRfilter))),
               cmap="gray", vmin=0, vmax=255)
    plt.title(f'Recovered image', fontname='Times New Roman', fontweight="bold")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = r'aerialpompeiiperiodic.jpg'
    periodic_noise_remove(file_path, n=3, D0=10)
