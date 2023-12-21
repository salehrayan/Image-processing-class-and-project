import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from skimage.transform import resize, rescale
import dtcwt

np.random.seed(42)

Original_image = cv2.imread(r'C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\pirate.tif', cv2.IMREAD_GRAYSCALE)
image_lowres = np.array(rescale(Original_image, 0.5))

transform = dtcwt.Transform2d()

wt = transform.forward(image_lowres, nlevels=1)


temp = np.zeros((wt.highpasses[0].shape[0]*2, wt.highpasses[0].shape[1]*2, 6), dtype='complex_')
for i in range(6):
    real_part = np.real(wt.highpasses[0][:, :, i])
    imaginary_part = np.imag(wt.highpasses[0][:, :, i])

    # Resize real and imaginary parts separately
    resized_real = cv2.resize(real_part, image_lowres.shape, interpolation=cv2.INTER_CUBIC)
    resized_imaginary = cv2.resize(imaginary_part, image_lowres.shape, interpolation=cv2.INTER_CUBIC)

    # Combine back into a complex array
    temp[:, :, i] = resized_real + 1j * resized_imaginary

wt.highpasses = (temp,)
wt.lowpass = cv2.resize(image_lowres, Original_image.shape, interpolation=cv2.INTER_CUBIC)
imrec = transform.inverse(wt)

plt.figure(figsize=(18, 10))
plt.subplot(132)
plt.imshow(imrec, cmap='gray')

plt.subplot(133)
plt.imshow(cv2.resize(image_lowres, Original_image.shape, interpolation=cv2.INTER_CUBIC), cmap='gray')


plt.tight_layout()
plt.show()

# plt.imshow(wt.lowpass, cmap='gray')
# plt.figure()
# plt.imshow(image_lowres, cmap='gray')
# plt.show()
