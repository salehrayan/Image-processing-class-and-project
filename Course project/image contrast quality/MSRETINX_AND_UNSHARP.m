clear; clc; close all;

image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image2.bmp');
image = rgb2gray(image);
[h, w, ~] = size(image);
image = imresize(image, [min([h w]) min([h w])], "bicubic");

retin = MSRetinex2(double(image), [15 80 250].*2.5, [1 1], 8);

% retin = imsharpen(double(image), 'Amount', 4, 'Radius', 2.5);

figure
imshow(retin, [0 255])
figure
imshow(image, [0 255])

[renyi_aiq_original, ~, ~] = RENYI_AQI(image,8,6,0,'degree','gray','common');
[renyi_aiq_enhanced, ~, ~] = RENYI_AQI(retin,8,6,0,'degree','gray','common');
% [wece_aiq_original, ~ , ~] = WECE_AQI(double(image)./255,8,6,0,'degree','gray','common');
% [wece_aiq_enhanced, ~, ~] = WECE_AQI(retin./255,8,6,0,'degree','gray','common');

disp(['Multi-scale Retinex'])
disp(['entropy: ' num2str(entropy(uint8(retin))) ', SSIM: ' num2str(ssim(uint8(retin),uint8(image)))])
disp(['AMBE: ' num2str(AMBE(image, retin)) ', EMEE: ' num2str(emee(retin, 8, 1))])
fprintf('Rényi-AIQ original: %.10f, Rényi-AIQ enhanced: %0.10f\n', renyi_aiq_original, renyi_aiq_enhanced);
% fprintf('WECE-AIQ original: %.10f, WECE-AIQ enhanced: %0.10f\n', wece_aiq_original, wece_aiq_enhanced);
disp(' ')




