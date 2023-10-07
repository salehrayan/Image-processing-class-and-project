import cv2
import matplotlib.pyplot as plt
import numpy as np

def zero_pad_gray(image, pad_top, pad_bottom, pad_left, pad_right):
    # Get the dimensions of the original image
    height, width = image.shape

    # Create a new blank image with the desired dimensions
    new_height = height + pad_top + pad_bottom
    new_width = width + pad_left + pad_right
    padded_image = np.zeros((new_height, new_width), dtype=np.uint8)

    # Copy the original image to the center of the padded image
    padded_image[pad_top:pad_top + height, pad_left:pad_left + width] = image

    return padded_image


