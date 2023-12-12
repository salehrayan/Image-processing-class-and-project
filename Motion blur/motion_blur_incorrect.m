clc;clear;close all;

image = imread('book.jpg');
[height, width] = size(image);
image_fft = fft2(image);
psf = fspecial('motion', 68, -45);

T = 1;
a = 0.1;
b = 0.1;

u_temp = 0:height-1;
v_temp = 0:width-1;
[v, u] = meshgrid(v_temp,u_temp); 

s = (pi.*(a.*u + b.*v));
psf_fft = (T./s).* sin(s).* exp(-1j.*s);
psf_fft(isnan(psf_fft)) = T;


figure
imshow(real(ifft2(image_fft.*psf_fft)), [0 255])

figure
imshow(imfilter(image, psf, 'conv','circular', 'same'), [0 255])
