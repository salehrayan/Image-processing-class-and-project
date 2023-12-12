clc;clear;close all;

image = imread('book.jpg');
[height, width] = size(image);
image_fft = fftshift(fft2(image));

n=10;      %butter order
D0 = 70;        %cutoff frequency
T = 1;          %shutter time
a = 0.1;
b = 0.1;
K = 0.005;      %Wiener constant


u_temp = -height/2:height/2-1;
v_temp = -width/2:width/2-1;
[v, u] = meshgrid(v_temp,u_temp); 

s = (pi.*(a.*u + b.*v));
motion_tf = (T./s).* sin(s).* exp(-1j.*s);          %blur_kernel
motion_tf(isnan(motion_tf)) = T;

inverse_motion_tf = 1./motion_tf;        %inverse_filter
inverse_motion_tf(abs(motion_tf) <1e-6) = 1;

x_temp = linspace(-height/2, height/2, height);
y_temp = linspace(-width/2, width/2, width);
[Y, X] = meshgrid(x_temp, y_temp);
butter_lowpass = 1./(1 + (hypot(Y, X)./D0).^(2*n));         %butter_lowpass
ideal_lowpass = zeros([height width]);
ideal_lowpass(hypot(Y, X)<D0) = 1;              %ideal_lowpass

wiener_filter = conj(motion_tf)./(abs(motion_tf).^2 + K);

blured_image = ifft2(ifftshift(image_fft.*motion_tf));
blured_image_fft = fftshift(fft2(blured_image));
std1 = 50;
std2 = 20;
std3 = 5;

noise1 =std1.* randn(size(image_fft));
noise2 =std2.* randn(size(image_fft));
noise3 =std3.* randn(size(image_fft));
degraded_im1 = blured_image+noise1;
degraded_im2 = blured_image+noise2;
degraded_im3 = blured_image+noise3;

degraded_im1_fft = fftshift(fft2(degraded_im1));
degraded_im2_fft = fftshift(fft2(degraded_im2));
degraded_im3_fft = fftshift(fft2(degraded_im3));




f = figure;
f.Position = [336.3333   41.6667  982.0000  946.0000];

size = 0.28;
s1 = subplot(331);
s1.Position(3:4) = [size size];
imshow(real(degraded_im1), [])

s4 = subplot(334);
s4.Position(3:4) = [size size];
imshow(real(degraded_im2), [])

s7 = subplot(337);
s7.Position(3:4) = [size size];
imshow(real(degraded_im3), [])

s2 = subplot(3,3,2);
s2.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im1_fft.*inverse_motion_tf.*butter_lowpass))), [])

s5 = subplot(3,3,5);
s5.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im2_fft.*inverse_motion_tf.*butter_lowpass))), [])

s8 = subplot(3,3,8);
s8.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im3_fft.*inverse_motion_tf.*butter_lowpass))), [])

s3 = subplot(3,3,3);
s3.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im1_fft.*wiener_filter))), [])

s6 = subplot(3,3,6);
s6.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im2_fft.*wiener_filter))), [])

s9 = subplot(3,3,9);
s9.Position(3:4) = [size size];
imshow(real(ifft2(ifftshift(degraded_im3_fft.*wiener_filter))), [])
