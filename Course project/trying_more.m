clc; clear; close all;

image_original = imread('pirate.tif');
% image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = imresize(image_original, 1./2, "bicubic");
alpha = 9;

% wt = dddtree2('realdt', image_lower_res, 2,'FSfarras','qshift10');

fname = 'nearsym5_7';
[LoD,HiD,LoR,HiR] = qbiorthfilt(fname);

[cA1,cH1,cV1,cD1] = dwt2(image_lower_res,[0 0 LoD' 0]',[0 HiD']');
[cA2,cH2,cV2,cD2] = dwt2(image_lower_res,[0 0 LoD' 0]',[0 HiD']');

cH1 = imresize(cH1, alpha, "bicubic");
cH2 = imresize(cH2, alpha, "bicubic");
cV1 = imresize(cV1, alpha, "bicubic");
cV2 = imresize(cV2, alpha, "bicubic");
cD1 = imresize(cD1, alpha, "bicubic");
cD2 = imresize(cD2, alpha, "bicubic");

cA1 = imresize(image_lower_res, size(cH1), "bicubic");
cA2 = imresize(image_lower_res, size(cH1), "bicubic");

imrec1 = idwt2(cA1,cH1,cV1,cD1, [0 0 LoD' 0]',[0 HiD']');
imrec2 = idwt2(cA2,cH2,cV2,cD2, [0 0 LoD' 0]',[0 HiD']');

imrec = imresize((imrec1+imrec2), size(image_original), 'bicubic');

imshow(imrec, [])
imrec = ((imrec1+imrec2) - min((imrec1+imrec2), [], 'all'))./(max((imrec1+imrec2), [], 'all')-...
    min((imrec1+imrec2), [], 'all')).*255;

disp(psnr(imresize(image_lower_res, size(image_original), "bicubic"), image_original))
disp(psnr(uint8(round(imrec)), image_original, 255))

disp(snr(double(image_original),...
    double(imresize(image_lower_res, size(image_original), "bicubic")-image_original)))
disp(snr(double(image_original), double(round(imrec))-double(image_original)))
