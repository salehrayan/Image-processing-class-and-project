clear; clc; close all;


figure
for parameter = 0.5:0.5:10
    fun(parameter)
  
end
    
    
function result = fun(parameter)

    image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image2.bmp');
    [h, w, ~] = size(image);
    image = rgb2gray(image(1:h-mod(h,16), 1:w-mod(w,16), :));
%     image = image./(max(image, [], 'all'));
    image = wdenoise2(image, 'DenoisingMethod', 'SURE');

    [A,H,V,D] = swt2(image,4,'haar');
    cutoff = my_iswt2_second(A,H,V,D, 'haar');
    my_sigma = cutoff./3;
    g = [1 1 1 1].*[parameter parameter+1 parameter+0.5 parameter].* my_sigma .*2.5;
    
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
%     result = -1.*entropy(uint8(enhanced))-1.*MCMA(image, enhanced) - ssim(uint8(enhanced),uint8(image));
    result = -1.*entropy(uint8(enhanced))- ssim(uint8(enhanced),uint8(image));
    disp(['entropy: ' num2str(entropy(uint8(enhanced))) ', SSMI: ' num2str(ssim(uint8(enhanced),uint8(image)))])
    imshow(uint8(enhanced), [0 255])
    title(['Parameter = ' num2str(parameter)])
    waitforbuttonpress;
end




function 





