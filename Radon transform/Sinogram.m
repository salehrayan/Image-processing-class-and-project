clc; clear;close all;


image_real = imread('SheppLogan_Phantom.svg.png');
image_real = imresize(image_real(:, :, 1), [512, 512]);
image = padarray(image_real, [0 0], 0, 'both');
[height, width] = size(image);


y_theta = 0:0.3:179.5;

x = (1-width)./2:(width-1)./2;
y = (1-height)./2:(height-1)./2;

radon_image = radon(image, y_theta);
radon_image = imrotate(radon_image, 90);

% for ro=1:size(x_ro, 2)
%     for theta = 1:360
%         temp = imrotate(image, -1.*y_theta(theta), 'nearest','crop');
%         radon_image(theta, ro) = sum(temp(:, ro), 'all');
%     end
% end

sinogram_image = zeros(height, width);
ro_index = x.*cos(y_theta.*pi./180) + y.*sin(y_theta.*pi./180);

imshow(radon_image, [])
% for y=1:height
%     for x=1:width

for row=1:height
    for col=1:width
        sinogram_image(row, col) = sum(radon_image(round(x.)))
        








