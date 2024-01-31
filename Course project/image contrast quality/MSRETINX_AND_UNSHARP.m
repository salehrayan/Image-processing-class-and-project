clear; clc; close all;

image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image3.bmp');
image = rgb2gray(image);
% image = wdenoise2(image, 'DenoisingMethod', 'SURE');
[h, w, ~] = size(image);
image = imresize(image, [min([h w]) min([h w])], "bicubic");

retin = MSRetinex2(double(image), [15 80 250].*1, [1 1], 8);
retin = min_max(retin)+20;
retin(retin<0) =0; retin(retin>255) = 255;

% retin = imsharpen(double(image), 'Amount', 2, 'Radius', 2);

figure
imshow(retin, [0 255])
figure
imshow(image, [0 255])

[renyi_aiq_original, ~, ~] = RENYI_AQI(image,8,6,0,'degree','gray','common');
[renyi_aiq_enhanced, ~, ~] = RENYI_AQI(retin,8,6,0,'degree','gray','common');
% [wece_aiq_original, ~ , ~] = WECE_AQI(double(image)./255,8,6,0,'degree','gray','common');
% [wece_aiq_enhanced, ~, ~] = WECE_AQI(retin./255,8,6,0,'degree','gray','common');
[Gmag, ~] = imgradient(retin, 'intermediate');

disp(['Multi-scale Retinex'])
disp(['entropy: ' num2str(entropy(uint8(retin))) ', SSIM: ' num2str(ssim(uint8(retin),uint8(image)))])
disp(['AMBE: ' num2str(AMBE(image, retin)) ', EMEE: ' num2str(emee(retin, 16, 1)) ', EME: ' num2str(eme(retin,23,16))])
disp(['AME: ' num2str(ame(retin, 16)) ', AMEE: ' num2str(amee(retin, 16,1)) ', MCMA: ' num2str(MCMA(image, retin))])
disp(['Edge content: ' num2str(mean(Gmag,"all")) ', HS: ' num2str(HS(retin))])    
fprintf('Rényi-AIQ original: %.10f, Rényi-AIQ enhanced: %0.10f\n', renyi_aiq_original, renyi_aiq_enhanced);
% fprintf('WECE-AIQ original: %.10f, WECE-AIQ enhanced: %0.10f\n', wece_aiq_original, wece_aiq_enhanced);
disp(' ')



function result = HS(im)
    [counts,~] = imhist(uint8(im));
    cumulative_sum_image = cumsum(counts)./max(cumsum(counts));
    quartiles = find((abs(cumulative_sum_image-0.75) <0.05)+ (abs(cumulative_sum_image-0.25) <0.05));
    result = (quartiles(end) - quartiles(1))./255;
end

function result = min_max(image)
    result = 255.*(image-min(image,[], "all"))./(max(image, [], "all") - min(image,[], "all"));
end





