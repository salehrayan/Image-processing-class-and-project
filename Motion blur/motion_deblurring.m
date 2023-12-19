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


t1 = real(ifft2(ifftshift(degraded_im1_fft.*inverse_motion_tf.*butter_lowpass)));
snrt1 = 10.*log(sum(t1.^2, 'all')./sum((t1-double(image)).^2, 'all'));
rmset1 = sqrt(mean((t1-double(image)).^2, 'all'));
psnrt1 = 10.*log(max(t1, [], 'all').^2./ (rmset1).^2);

t2 = real(ifft2(ifftshift(degraded_im2_fft.*inverse_motion_tf.*butter_lowpass)));
snrt2 = 10.*log(sum(t2.^2, 'all')./sum((t2-double(image)).^2, 'all'));
rmset2 = sqrt(mean((t2-double(image)).^2, 'all'));
psnrt2 = 10.*log(max(t2, [], 'all').^2./ (rmset2).^2);

t3 = real(ifft2(ifftshift(degraded_im3_fft.*inverse_motion_tf.*butter_lowpass)));
snrt3 = 10.*log(sum(t3.^2, 'all')./sum((t3-double(image)).^2, 'all'));
rmset3 = sqrt(mean((t3-double(image)).^2, 'all'));
psnrt3 = 10.*log(max(t1, [], 'all').^2./ (rmset3).^2);

x1 = real(ifft2(ifftshift(degraded_im1_fft.*wiener_filter)));
snr1 = 10.*log(sum(x1.^2, 'all')./sum((x1-double(image)).^2, 'all'));
rmse1 = sqrt(mean((x1-double(image)).^2, 'all'));
psnr1 = 10.*log(max(x1, [], 'all').^2./ (rmse1).^2);

x2 = real(ifft2(ifftshift(degraded_im2_fft.*wiener_filter)));
snr2 = 10.*log(sum(x2.^2, 'all')./sum((x2-double(image)).^2, 'all'));
rmse2 = sqrt(mean((x2-double(image)).^2, 'all'));
psnr2 = 10.*log(max(x2, [], 'all').^2./ (rmse2).^2);

x3 = real(ifft2(ifftshift(degraded_im3_fft.*wiener_filter)));
snr3 = 10.*log(sum(x3.^2, 'all')./sum((x3-double(image)).^2, 'all'));
rmse3 = sqrt(mean((x3-double(image)).^2, 'all'));
psnr3 = 10.*log(max(x3, [], 'all').^2./ (rmse3).^2);

f = figure;
f.Position = [336.3333   41.6667  982.0000  946.0000];

size = 0.27;
s1 = subplot(331);
s1.Position(3:4) = [size size];
imshow(real(degraded_im1), [0 255])
title(['noise variance: ' num2str(std1.^2) ])

s4 = subplot(334);
s4.Position(3:4) = [size size];
imshow(real(degraded_im2), [0 255])
title(['noise variance: ' num2str(std2.^2) ])

s7 = subplot(337);
s7.Position(3:4) = [size size];
imshow(real(degraded_im3), [0 255])
title(['noise variance: ' num2str(std3.^2) ])

s2 = subplot(3,3,2);
s2.Position(3:4) = [size size];
imshow(t1, [])
title(['SNR: ' num2str(snrt1) ', RMSE: ' num2str(rmset1)])

s5 = subplot(3,3,5);
s5.Position(3:4) = [size size];
imshow(t2, [])
title(['SNR: ' num2str(snrt2) ', RMSE: ' num2str(rmset2)])

s8 = subplot(3,3,8);
s8.Position(3:4) = [size size];
imshow(t3, [])
title(['SNR: ' num2str(snrt3) ', RMSE: ' num2str(rmset3)])

s3 = subplot(3,3,3);
s3.Position(3:4) = [size size];
imshow(x1, [])
title(['SNR: ' num2str(snr1) ', RMSE: ' num2str(rmse1)])

s6 = subplot(3,3,6);
s6.Position(3:4) = [size size];
imshow(x2, [])
title(['SNR: ' num2str(snr2) ', RMSE: ' num2str(rmse2)])

s9 = subplot(3,3,9);
s9.Position(3:4) = [size size];
imshow(x3, [])
title(['SNR: ' num2str(snr3) ', RMSE: ' num2str(rmse3)])
