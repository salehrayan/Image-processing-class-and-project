clc; clear;close all;


image_real = imread('SheppLogan_Phantom.svg.png');
image_real = imresize(image_real(:, :, 1), [256, 256]);
image = padarray(image_real, [90 90], 0, 'both');
[height, width] = size(image);


accumulation = 0;
y_theta = 179.5:-0.5:0;
% x_ro =  ((1-max([width height]))./2-0.5:0.5:(max([width height])-1)./2+0.5);
x_ro = (1-height)./2: (height-1)./2;

radon_image = zeros([360 size(x_ro, 2)]);

for ro=1:size(x_ro, 2)
    for theta = 1:360
        temp = imrotate(image, -1.*y_theta(theta), 'nearest','crop');
        radon_image(theta, ro) = sum(temp(:, ro), 'all');
    end
end

% t = imrotate(image, 0);
% imshow(imrotate(image, 129, 'nearest','crop'), [])
figure()
imshow(imresize(radon_image, 2), [])
title('Manual Radon transform')
figure
imshow(imresize(radon(image, 0:0.5:179.5), 2), [])
title('Matlab Radon transform')