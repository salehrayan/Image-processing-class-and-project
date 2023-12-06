clc;clear;close all;


image = imread('book.jpg');
[height, width] = size(image);
image_fft = fft2(image);
psf = fspecial('motion', 15, 45);

% nx = 20;
% ny = 20;
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
imshow(log(abs(psf_fft)), [])

figure
imshow(log(abs(fftshift(psf_fft))), [])

figure
imshow(real(ifft2(psf_fft)), [])

figure
imshow(log(abs(fftshift(fft2(psf,height,width)))), [])

figure
imshow(real(ifft2(image_fft.*psf_fft)), [])

figure
imshow(imfilter(image, psf, 'conv','circular', 'same'), [])
