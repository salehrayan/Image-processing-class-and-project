import cv2
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt



shear_vertical_factor = 0.2
shear_horizontal_factor = 0.7


'Making T'
shape = 400
image_T = np.zeros((shape, shape), dtype=np.uint8)
image_T[:,:] = 128

middle = math.floor(shape / 2)
t_c_h = math.floor(shape / 3.2)
t_c_w = math.floor(shape / 20)
t_h_h = math.floor(1.6 * shape / 20)
t_h_w = math.floor(t_c_h / 1.5)

image_T[middle - t_c_h: middle+t_c_h, middle-t_c_w: middle+t_c_w] = 255
image_T[middle - t_c_h: middle - t_c_h + t_h_h, middle-t_h_w: middle+t_h_w] = 255



"""shear transform"""
shear_vertical_matrix = np.float32([[1, 0, 0],  # 0.5 is the shearing factor
                           [shear_vertical_factor, 1, 0],
                           [0,0,1]])
shear_horizontal_matrix = np.float32([[1, shear_horizontal_factor, 0],  # 0.5 is the shearing factor
                           [0, 1, 0],
                           [0,0,1]])

sheared_image = cv2.warpPerspective(image_T, shear_vertical_matrix, (image_T.shape[1],
                                    image_T.shape[0]+int(image_T.shape[0]*shear_vertical_factor)))
sheared_image_final = cv2.warpPerspective(sheared_image, shear_horizontal_matrix,
                                    (sheared_image.shape[1]+int(sheared_image.shape[0]*shear_horizontal_factor),
                                        sheared_image.shape[0]))

"""Solving 8 equations 8 unknowns"""
# points_in_sheared = np.array([[130,211], [152,327], [131, 371], [361, 432]], dtype=np.float32)
# points_in_original = np.array([[106,117], [107,220], [75, 282], [325, 180]], dtype=np.float32)

# points_in_sheared = np.array([[366,473], [359,433], [160, 392], [101, 190]],dtype=np.float32)
# points_in_original = np.array([[324,219], [324,180], [106, 282], [75, 117]],dtype=np.float32)

points_in_sheared = np.array([[0,0], [398,280], [81, 454], [477, 731]],dtype=np.float32)
points_in_original = np.array([[0,0], [399,0], [0, 399], [399, 399]],dtype=np.float32)

A = np.empty((4,4))
B_for_height = np.empty([4])
B_for_width = np.empty([4])
for i in range(4):
    aheight = points_in_sheared[i,0]
    awidth = points_in_sheared[i,1]
    A_temp = np.array([aheight, awidth, aheight*awidth, 1])
    A[i] = A_temp
    B_for_height[i] = points_in_original[i,0]
    B_for_width[i] = points_in_original[i,1]

solutions_for_height = np.linalg.solve(A, B_for_height)
solutions_for_width = np.linalg.solve(A, B_for_width)

"""Restoring image from transform"""
restored_image = np.zeros((shape,shape))
for height_of_sheared in tqdm(range(sheared_image_final.shape[0])):
    for width_of_sheared in range(sheared_image_final.shape[1]):

        height_of_restored = int(np.matmul(np.array([height_of_sheared, width_of_sheared,
                                                 height_of_sheared*width_of_sheared, 1]), solutions_for_height))
        width_of_restored = int(np.matmul(np.array([height_of_sheared, width_of_sheared,
                                                 height_of_sheared*width_of_sheared, 1]), solutions_for_width))
        if height_of_restored < 0 or height_of_restored >=shape or width_of_restored < 0 or width_of_restored >= shape:
            continue

        restored_image[height_of_restored,width_of_restored] = sheared_image_final[height_of_sheared, width_of_sheared]
        if restored_image[height_of_restored,width_of_restored] == 0:
            t = 4

"""Enhancing restored image"""
restored_image_mean = restored_image.copy()
for h in tqdm(range(restored_image_mean.shape[0])):
    for w in range(restored_image_mean.shape[1]):
        if restored_image_mean[h,w] == 0:
            restored_image_mean[h,w] = int((restored_image_mean[max(h-1,0), w] + restored_image_mean[min(h+1, shape-1), w] +
                                       restored_image_mean[h, max(w-1,0)] + restored_image_mean[h, min(w+1,shape-1)] +
                                    restored_image_mean[max(h-1,0),max(w-1,0)] +
                                    restored_image_mean[max(h-1,0),min(w+1,shape-1)] +
                                            restored_image_mean[min(h+1,shape-1), min(w+1, shape-1)]+
                                            restored_image_mean[min(h+1,shape-1), max(w-1, 0)]) / 8)

difference = abs(image_T - restored_image_mean)


fig = plt.figure(figsize=(9,10))
ax1 = plt.subplot(321)
ax1.imshow(image_T, cmap='gray', vmin=0, vmax=255)
ax1.set_title('Original Image', fontname='Times New Roman', fontweight="bold")

ax2 = plt.subplot(322)
ax2.imshow(sheared_image_final, cmap='gray', vmin=0, vmax=255)
ax2.set_title(f'Sheared Image', fontname='Times New Roman', fontweight="bold")
for point in points_in_sheared:
    ax2.scatter(point[1], point[0], s=20, c='red', marker='o')

ax3 = plt.subplot(323)
ax3.imshow(restored_image, cmap='gray', vmin=0, vmax=255)
ax3.set_title(f'Restored Image', fontname='Times New Roman', fontweight="bold")

ax4 = plt.subplot(324)
ax4.imshow(restored_image_mean, cmap='gray', vmin=0, vmax=255)
ax4.set_title(f'Restored Image With Mean Of Neighbours', fontname='Times New Roman', fontweight="bold")

ax5 = plt.subplot(325)
ax5.imshow(difference, cmap='gray', vmin=0, vmax=255)
ax5.set_title(f'Difference', fontname='Times New Roman', fontweight="bold")

plt.tight_layout()
plt.show()