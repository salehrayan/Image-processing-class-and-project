clc;clear;close all;

image = imread(['C:\Users\ASUS\Desktop\Image processing\' ...
    'Rotate and resize\standard_test_images\house.tif']);
image = image(:, : , 1);
figure
imshow(image, [0 255])
title('Original image')
[h, w] = size(image);

image_fft = fftshift(fft2(image, h+50, w+50));
D0 = 40;
n=2;

x_temp = linspace(-h/2, h/2, h+50);
y_temp = linspace(-w/2, w/2, w+50);

[Y, X] = meshgrid(x_temp, y_temp);

ideal_lowpass = zeros([h+50 w+50]);
ideal_lowpass(hypot(Y, X)<D0) = 1;
butter_lowpass = 1./(1 + (hypot(Y, X)./D0).^(2*n));
gaussain_lowpass = exp(-(hypot(Y, X)).^2/(2.*(D0.^2)));

result_ideal = real(ifft2(ifftshift(image_fft.*ideal_lowpass)));
result_butter = real(ifft2(ifftshift(image_fft.*butter_lowpass)));
result_gaussian = real(ifft2(ifftshift(image_fft.*gaussain_lowpass)));
figure(WindowState="maximized")

subplot(2,3,1)
mesh(Y, X, ideal_lowpass)
title(['Ideal low-pass filter, cutoff = ' num2str(D0)])

subplot(2,3,2)
mesh(Y, X, butter_lowpass)
title(["Butterwoth low-pass filter, cutoff = "+num2str(D0) "n = "+num2str(n)])

subplot(2,3,3)
mesh(Y, X, gaussain_lowpass)
title("Gaussian low-pass filter, cutoff = "+num2str(D0))

subplot(2,3,4)
imshow(result_ideal(1:h, 1:w), [0 255])

subplot(2,3,5)
imshow(result_butter(1:h, 1:w), [0 255])

subplot(2,3,6)
imshow(result_gaussian(1:h, 1:w), [0 255])
