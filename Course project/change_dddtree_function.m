clc; clear; close all;

image_original = imread('WDC_ADS40_Color_6Inch_2-web.jpg');
image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = single(imresize(image_original, 1./2, "bicubic"));
alpha = 2; beta = 1;