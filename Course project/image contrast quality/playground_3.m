clc; clear; close all;
image = imread( ...
    ['C:\Users\ASUS\Desktop\Image processing\Course project\' ...
    'Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image2.bmp']);
image = rgb2gray(image(1:end-4, 1:end-12, :));
image = wdenoise2(image, 'DenoisingMethod', 'SURE');
% [counts1,binLocations1] = imhist(uint8(image));

% cumulative_sum_image = cumsum(counts1)./max(cumsum(counts1));

% figure
% stem(0:255, cumulative_sum_image)
% quartiles = find((abs(cumulative_sum_image-0.75) <1e-3)+ (abs(cumulative_sum_image-0.25) <1e-3));
% (quartiles(2) - quartiles(1))./255
HS(image)


image = imread( ...
    ['C:\Users\ASUS\Desktop\Image processing\Course project\' ...
    'Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image2_enhanced1.bmp']);
image = rgb2gray(image(1:end-4, 1:end-12, :));

image = wdenoise2(image, 'DenoisingMethod', 'SURE');

figure
imhist(uint8(image))
HS(image)



function result = HS(image)
    [counts,~] = imhist(uint8(image));
    cumulative_sum_image = cumsum(counts)./max(cumsum(counts));
    quartiles = find((abs(cumulative_sum_image-0.75) <0.05)+ (abs(cumulative_sum_image-0.25) <0.05));
    result = (quartiles(end) - quartiles(1))./255;
end






