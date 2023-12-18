clc;clear;close all;


image = imread('SheppLogan_Phantom.svg.png');
image = imresize(image(:, :, 1), [256, 256]);

[height, width] = size(image);

x = linspace((1-width)./2 , (width-1)./2, width);
y = linspace((1-height)./2 , (height-1)./2, height);

[X , Y] = meshgrid(x, y);

accumulation = 0;
x_theta = 179.5:-0.5:0;
y_ro = (1-max([width height]))./2-0.5:0.5:(max([width height])-1)./2+0.5;

radon_image = zeros([360 513]);

for ro=1:513
    for theta=1:360
        radon_image(theta, ro) = sum(image(abs(X.*cos(x_theta(theta).*pi./180) + Y.*sin(x_theta(theta).*pi./180)-y_ro(ro))<=0.5), 'all');
    end
end
imshow(radon_image, [])

