clc; clear; close all;

image_original = imread('mandrill.png');
image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = single(imresize(image_original, 1./2, "bicubic"));
alpha = 2; beta = 1;

[Faf, Fsf] = FSfarras;
[af, sf] = dualfilt1;
w = cplxdual2D(image_lower_res, 1, Faf, af);

imrec = imresize(icplxdual2D(w, 1, Faf, af, double(image_lower_res)), 0.5);


figure
imshow(image_lower_res, [0 255])
title('Low resolution image')

figure
imshow(image_original, [0 255])
title('Original Image')

im_bicub = imresize(image_lower_res, alpha, "bicubic");
tiledlayout(1,2)

% First plot
ax1 = nexttile;
imshow(im_bicub, [0 255])
title('Bicubic interpolation')

% Second plot
ax2 = nexttile;
imshow(imrec, [0 255])
title('CWT-super resolution')

linkaxes([ax1 ax2],'xy')

disp(psnr(im_bicub, single(image_original), 255))
% MSE = mean((im_bicub - double(image_original)).^2, "all");
% disp(10.*log10((255.^2)./MSE))
disp(psnr(uint8(round(imrec(1:end, 1:end))), image_original, 255))
