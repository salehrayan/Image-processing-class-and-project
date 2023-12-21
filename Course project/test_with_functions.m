clc; clear; close all;

image_original = imread('WDC_ADS40_Color_6Inch_2-web.jpg');
image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = double(imresize(image_original, 1./2, "bicubic"));
alpha = 2; 

[Faf, Fsf] = FSfarras;
[af, sf] = dualfilt1;
w = cplxdual2D(image_lower_res, 1, Faf, af);

w{2}{1}{1} = double(image_lower_res);
w{2}{1}{2} = double(image_lower_res);
w{2}{2}{1} = double(image_lower_res);
w{2}{2}{2} = double(image_lower_res);

for i=[1 2]
    for j=[1 2]
        for k=[1 2 3]
            w{1}{i}{j}{k} = double(imresize(w{1}{i}{j}{k}, alpha, 'bicubic'));
        end
    end
end

imrec = imresize(icplxdual2D(w, 1, Fsf, sf), 1./alpha.*2, "bicubic");

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

disp(psnr(uint8(imresize(image_lower_res, size(image_original), "bicubic")), uint8(image_original)))
disp(psnr(uint8(round(imrec)), image_original, 255))

% disp(snr(double(image_original),...
%     double(imresize(image_lower_res, size(image_original), "bicubic")-image_original)))
% disp(snr(double(image_original), double(round(imrec))-double(image_original)))



