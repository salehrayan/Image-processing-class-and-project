import numpy as np
import matplotlib.pyplot as plt
import cv2

from scipy.signal import convolve2d as conv2

from skimage import color, data, restoration



astro = cv2.imread(r'C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.02.tiff', cv2.IMREAD_GRAYSCALE)
astro2 = cv2.imread(r'C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.02.tiff', cv2.IMREAD_GRAYSCALE)

psf = np.ones((4, 4)) / 16
astro = conv2(astro, psf, 'same')

# Add Noise to Image
astro_noisy = astro.copy() +  40* np.random.randn(astro.shape[0], astro.shape[1])

astro_noisy = (astro_noisy-np.min(astro_noisy))/(np.max(astro_noisy)-np.min(astro_noisy))
# Restore Image using Richardson-Lucy algorithm
deconvolved_RL = restoration.wiener(astro_noisy, psf, balance= 0.3)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 5))
plt.gray()

for a in (ax[0], ax[1], ax[2]):
       a.axis('off')

ax[0].imshow(astro2)
ax[0].set_title('Original Data')

ax[1].imshow(astro_noisy)
ax[1].set_title('Noisy data')

ax[2].imshow(deconvolved_RL)
ax[2].set_title('Restoration using\nRichardson-Lucy')


fig.subplots_adjust(wspace=0.02, hspace=0.2,
                    top=0.9, bottom=0.05, left=0, right=1)
plt.show()