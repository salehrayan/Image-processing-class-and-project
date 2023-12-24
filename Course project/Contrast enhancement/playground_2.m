clc;clear; close all;

image = imread('cropped_1.jpg');
image = rgb2gray(image(1:end, 1:end-15, :));
image = wdenoise2(image, 'DenoisingMethod', 'SURE');
figure()
imshow(image, [])
d0 = 100;
[A,H,V,D] = swt2(image,4,'haar');

my_sigma = [2.5 6.5 10 10];
g = [0.1 1.1 2.5 2];
a = 1;
b = 0;
gamma = 1;

% A(:,:,4) = normalize(A(:,:,4), 'range').*255;
% H(abs(H)>70) = 0;
% V(abs(V)>70) = 0;  g(j).*pdf('Normal', H(:,:,j)+V(:,:,j)+D(:,:,j), 0, my_sigma(j))
% D(abs(D)>70) = 0;
x_hat = 0;
% for j=4:-1:1
%     temp =A(:,:,j) + H(:,:,j)+V(:,:,j)+D(:,:,j);
% %     temp(temp>d0) = d0;
% %     temp(temp<-d0) = -d0;
%     x_hat = x_hat + temp ;
% end

figure
imshow(my_iswt2(A,H,V,D, 'haar'), [0 255])





function t = min_max(x)

t = (x - min(x,[], 'all'))./(max(x, [], "all") - min(x, [], 'all')).*255;
end

