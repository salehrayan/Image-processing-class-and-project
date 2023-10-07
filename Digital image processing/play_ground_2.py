import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image = cv2.imread('standard_test_images/cameraman.tif', cv2.IMREAD_GRAYSCALE)

# Define the number of pixels to pad in each direction (top, bottom, left, right)
pad_top = 20
pad_bottom = 20
pad_left = 30
pad_right = 30

# Get the dimensions of the original image
height, width = image.shape

# Create a new blank image with the desired dimensions
new_height = height + pad_top + pad_bottom
new_width = width + pad_left + pad_right
padded_image = np.zeros((new_height, new_width), dtype=np.uint8)

# Copy the original image to the center of the padded image
padded_image[pad_top:pad_top + height, pad_left:pad_left + width] = image

plt.imshow(padded_image, cmap='gray')
plt.show()

