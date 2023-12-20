clc;clear; close all;

image = imread('Ottawa-15.tif');
[J, rect] = imcrop(image);

imwrite(J, 'cropped_1.jpg')
