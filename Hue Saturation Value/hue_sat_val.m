clc;clear;close all;

image = imread("C:\Users\ASUS\Desktop\Image processing\Rotate and resize\standard_test_images\peppers_color.jpg");

image_hsv = rgb2hsv(image);


figure()
imshow(image, [0 255])

figure(WindowState="maximized")

subplot(231)
imshow(image(:,:,1), [0 255])
title('R')

subplot(232)
imshow(image(:,:,2), [0 255])
title('G')

subplot(233)
imshow(image(:,:,3), [0 255])
title('B')

subplot(234)
imshow(image_hsv(:,:,1), [0 1])
title('Hue')

subplot(235)
imshow(image_hsv(:,:,2), [0 1])
title('Saturation')

subplot(236)
imshow(image_hsv(:,:,3), [0 1])
title('Value')

