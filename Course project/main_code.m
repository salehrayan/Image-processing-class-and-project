clc;clear; close all;

alpha = 2;
beta = 6;
image_original = imread('jetplane.tif');
image_original = image_original(1:end,:, 1);
% image_original = rgb2gray(image_original(1:end, :, :));
image_original = imresize(image_original, [512, 512]);
image_lower_res = imresize(image_original, 1./alpha, "bicubic");


[a, d] = dualtree2(image_lower_res, 'Level',1);
[n, m] = dualtree2(image_original, 'Level',1);

b = d{1, 1};
b_replacement = zeros([size(m{1, 1},1)*beta size(m{1, 1},2)*beta  6]);

for i=1:6
    b_replacement(:, :, i) = imresize(b(:, 1:end, i), [size(m{1, 1},1)*beta size(m{1, 1},2)*beta], "bicubic");
end

b_replacement = {b_replacement};

imrec = idualtree2(imresize(image_lower_res, size(image_original)*beta, "bicubic"), b_replacement);
imrec = imresize(imrec, size(image_original));

figure
imshow(image_lower_res, [0 255])
title('Low resolution image')

figure
imshow(image_original, [0 255])
title('Original Image')

figure
imshow(imresize(image_lower_res, alpha, "bicubic"), [0 255])
title('Bicubic interpolation')

figure
imshow(imrec, [0 255])
title('CWT-super resolution')

disp(psnr(imresize(image_lower_res, size(image_original), "bicubic"), image_original))
disp(psnr(uint8(round(imrec)), image_original, 255))

disp(snr(double(image_original),...
    double(imresize(image_lower_res, size(image_original), "bicubic")-image_original)))
disp(snr(double(image_original), double(round(imrec))-double(image_original)))




