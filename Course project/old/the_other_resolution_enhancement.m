 clear; close all;

image_original = imread('mandrill.jpg');
image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = single(imresize(image_original, 1./2, "bicubic"));
alpha = 2; beta = 1;

c = wavecdf97(image_lower_res,1);
[h, w] = size(c);
temp = zeros(size(c)*2);


temp(1:h, 1:w) = image_lower_res;
temp(h+1:end, 1:w) = imresize(c(h/2+1:end , 1:w/2), 2);
temp(1:h, w+1:end) = imresize(c(1:h/2 , h/2+1:end), 2);
temp(h+1:end, w+1:end) = imresize(c(h/2+1:end , h/2+1:end), 2);


imrec = wavecdf97(temp, -1);
imshow(imrec, [])

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
