clc;clear;close all;


image = imread(['C:\Users\ASUS\Desktop\Image processing\' ...
    'Rotate and resize\standard_test_images\cameraman.tif']);
image = image(:, : , 1);
kernel = [-1 0 1
          -2 0 2
          -1 0 1];
[h, w] = size(image);

image_fft = fft2(image, h+3, w+3);
kernel_fft = fft2(kernel, h+3, w+3);
image_filtered_f = image_fft .* kernel_fft;


figure(WindowState="maximized")
subplot(2,3,1)
mesh(abs(fftshift(kernel_fft)))
title('Kernel FFT Mesh plot')
% freqz2(kernel, [h+3, w+3])

subplot(2,3,2)
imshow(abs(fftshift(kernel_fft)), [] , 'InitialMagnification', 'fit')
title('Kernel FFT')

subplot(2,3,3)
imshow(image, [] , 'InitialMagnification', 'fit')
title('Original image')

subplot(2,3,4)
imshow(log(abs(fftshift(image_fft)) + 1), [] , ...
    'InitialMagnification', 'fit')
title('FFT of image')

subplot(2,3,5)
imshow(real(ifft2(image_filtered_f)), [0 255], 'InitialMagnification', 'fit')
title('Image filtered in fourier domain')

subplot(2,3,6)
imshow(convolve2d(image, kernel), [0 255], 'InitialMagnification', 'fit')
title('image filtered in spatial domain')



function temp = convolve2d(im, ker)
    ker = -1 .* double(ker); 
    [hei, wid] = size(im);

    im_padded = double(padarray(im, [2 2], 0, 'both'));

    temp = zeros([hei+4 wid+4]);
    size_temp = size(temp);

    for row=1:size_temp(1)-2
        for col=1:size_temp(2)-2
            temp(row, col) = sum(im_padded(row:row+2, col:col+2) .* ker, 'all');
        end
    end
    temp = temp(3:end-2, 3:end-2);
end



