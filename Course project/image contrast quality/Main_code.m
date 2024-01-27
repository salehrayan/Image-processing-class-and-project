clear; clc; close all;

image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image2.bmp');
image = rgb2gray(image);
[h, w, ~] = size(image);
image = imresize(image, [min([h w]) min([h w])], "bicubic");
figure
for parameter = 2.5
    
    fun(parameter, image)
  
end
    
    
function result = fun(parameter, image)
    
    [h, w, ~] = size(image);
    image_original = image(1:h-mod(h,16), 1:w-mod(w,16), :);

    image = wdenoise2(image_original, 'DenoisingMethod', 'SURE');
    image(image<0) = 0; image(image>255) = 255;

    [A,H,V,D] = swt2(image,4,'haar');
    cutoff = my_iswt2_second(A,H,V,D, 'haar');
    my_sigma = cutoff./3;
    g = [1 1 1 1].*[parameter parameter+1 parameter+0.5 parameter].* my_sigma .*2.5;
    
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
    enhanced(enhanced<0) = 0; enhanced(enhanced>255) = 255;
    [renyi_aiq_original, ~, ~] = RENYI_AQI(image,8,6,0,'degree','gray','common');
    [renyi_aiq_enhanced, ~, ~] = RENYI_AQI(enhanced,8,6,0,'degree','gray','common');
%     [wece_aiq_original, ~, ~] = WECE_AQI(double,8,6,0,'degree','gray','common');
%     [wece_aiq_enhanced, ~, ~] = WECE_AQI(enhanced,8,6,0,'degree','gray','common');
    
    disp(['Parameter = ' num2str(parameter)])
    disp(['entropy: ' num2str(entropy(uint8(enhanced))) ', SSIM: ' num2str(ssim(uint8(enhanced),uint8(image)))])
    disp(['AMBE: ' num2str(AMBE(image_original, enhanced)) ', EMEE: ' num2str(emee(enhanced, 8, 1))])
    fprintf('Rényi-AIQ original: %.10f, Rényi-AIQ enhanced: %0.10f\n', renyi_aiq_original, renyi_aiq_enhanced);
%     disp(['WECE-AIQ original: ' num2str(wece_aiq_original) ', WECE-AIQ enhanced: ' num2str(wece_aiq_enhanced)])
    disp(' ')

    imshow(uint8(enhanced), [0 255])
    title(['Parameter = ' num2str(parameter)])
    waitforbuttonpress;
end







