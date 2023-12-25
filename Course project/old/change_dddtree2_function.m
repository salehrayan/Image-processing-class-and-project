clc; clear; close all;

image_original = imread('WDC_ADS40_Color_6Inch_2-web.jpg');
image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = single(imresize(image_original, 1./2, "bicubic"));
alpha = 2; beta = 1;

wt = dddtree2('cplxdt', image_lower_res, 1, 'FSfarras', 'qshift10');

temp = zeros([size(wt.cfs{2}, 1)*2 size(wt.cfs{2}, 2)*2 2 2]);
temp(:,:, 1, 1) = image_lower_res;
temp(:,:, 1, 2) = image_lower_res;
temp(:,:, 2, 1) = image_lower_res;
temp(:,:, 2, 2) = image_lower_res;
% wt2 = dddtree2('cplxdt', image_lower_res, 1, 'FSfarras', 'qshift10');
wt.cfs{2} = temp;

imrec = my_idddtree2(wt);

figure
imshow(image_lower_res, [0 255])
title('Low resolution image')

figure
imshow(image_original, [0 255])
title('Original Image')

tiledlayout(1,2)

% First plot
ax1 = nexttile;
imshow(imresize(image_lower_res, alpha, "bicubic"), [0 255])
title('Bicubic interpolation')

% Second plot
ax2 = nexttile;
imshow(imrec, [0 255])
title('CWT-super resolution')

linkaxes([ax1 ax2],'xy')


disp(psnr(imresize(image_lower_res, size(image_original), "bicubic"), single(image_original),255))
disp(psnr(uint8(round(imrec)), image_original, 255))
