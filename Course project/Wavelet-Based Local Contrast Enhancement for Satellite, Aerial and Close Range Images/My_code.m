clc;clear; close all;

image = imread('cropped_1.jpg');
image = rgb2gray(image(1:end, 1:end-15, :));
image = wdenoise2(image, 'DenoisingMethod', 'SURE');
figure()
imshow(image, [])
[A,H,V,D] = swt2(image,4,'haar');


figure
imshow(my_iswt2(A,H,V,D, 'haar'), [0 255])


function t = min_max(x)

t = (x - min(x,[], 'all'))./(max(x, [], "all") - min(x, [], 'all')).*255;
end

