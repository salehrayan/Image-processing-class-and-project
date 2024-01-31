clear; clc; close all;

image = imread('E:\Image processing\Course project\Mammogram images\mdb006.pgm');
% image = rgb2gray(image);
[h, w, ~] = size(image);
image = imresize(image, [min([h w]) min([h w])], "bicubic");
figure
for parameter = 0:0.5:8
    
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
    [Gmag, ~] = imgradient(enhanced, 'intermediate');
    
    disp(['Parameter = ' num2str(parameter)])
    disp(['entropy: ' num2str(entropy(uint8(enhanced))) ', SSIM: ' num2str(ssim(uint8(enhanced),uint8(image)))])
    disp(['AMBE: ' num2str(AMBE(image, enhanced)) ', EMEE: ' num2str(emee(enhanced, 16, 1)) ', EME: ' num2str(eme(enhanced,23,16))])
    disp(['AME: ' num2str(ame(enhanced, 16)) ', AMEE: ' num2str(amee(enhanced, 16,1)) ', MCMA: ' num2str(MCMA(image, enhanced))])
    disp(['Edge content: ' num2str(mean(Gmag,"all")) ', HS: ' num2str(HS(enhanced))])    
    fprintf('Rényi-AIQ original: %.10f, Rényi-AIQ enhanced: %0.10f\n', renyi_aiq_original, renyi_aiq_enhanced);
    %     disp(['WECE-AIQ original: ' num2str(wece_aiq_original) ', WECE-AIQ enhanced: ' num2str(wece_aiq_enhanced)])
    disp(' ')

    imshow(uint8(enhanced), [0 255])
    title(['Parameter = ' num2str(parameter)])
    waitforbuttonpress;
end

function result = HS(im)
    [counts,~] = imhist(uint8(im));
    cumulative_sum_image = cumsum(counts)./max(cumsum(counts));
    quartiles = find((abs(cumulative_sum_image-0.75) <0.05)+ (abs(cumulative_sum_image-0.25) <0.05));
    result = (quartiles(end) - quartiles(1))./255;
end





