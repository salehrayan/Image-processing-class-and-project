clc; clear; close all;

image_original = imread('pirate.tif');
% image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = imresize(image_original, 1./2, "bicubic");
alpha = 9;

[a, d] = my_dualtree2(image_lower_res, 'Level', 1);