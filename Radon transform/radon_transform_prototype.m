clc; clear;close all;


image = imread('SheppLogan_Phantom.svg.png');
image = imresize(image(:, :, 1), [256, 256]);

[height, width] = size(image);

x = (1-width)./2 : (width-1)./2;
y = (1-height)./2 : (height-1)./2;

[X , Y] = meshgrid(x, y);

accumulation = 0;
y_theta = 179.5:-0.5:0;
% x_ro =  ((1-max([width height]))./2-0.5:0.5:(max([width height])-1)./2+0.5);
x_ro = (1-width)./2-30 : (width-1)./2+30;

radon_image = zeros([360 size(x_ro, 2)]);
% figure()
% imshow(radon(image), [])
% abs(X.*cos(y_theta(theta).*pi./180) + Y.*sin(y_theta(theta).*pi./180)-x_ro(ro))<=0.5)

for ro=158
    for theta=270
        test = zeros([height width]);
        test( (x_ro(ro)-0.5  <= X.*cos(y_theta(theta).*pi./180) + Y.*sin(y_theta(theta).*pi./180)) &...
            X.*cos(y_theta(theta).*pi./180) + Y.*sin(y_theta(theta).*pi./180) <= x_ro(ro)+0.5) = 1;
        imshow(test, [])
        title(['ro=' num2str(x_ro(ro)) ', theta=' num2str(y_theta(theta)) ', theta index=' num2str(theta)])
        drawnow
        pause(300)
%         waitforbuttonpress
    end
end


for ro=1:size(x_ro, 2)
    for theta=1:360
        radon_image(theta, ro) = sum(image(...
            (x_ro(ro)-0.5001  < X.*cos(y_theta(theta).*pi./180) + Y.*sin(y_theta(theta).*pi./180)) &...
            X.*cos(y_theta(theta).*pi./180) + Y.*sin(y_theta(theta).*pi./180) < x_ro(ro)+0.5001), 'all');
    end
end
imshow(imresize(radon_image, 2), [])

