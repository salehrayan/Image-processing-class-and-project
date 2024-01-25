clear; clc; close all;


figure
for parameter = 0:0.5:10
    fun(parameter)
  
end
    
    
function result = fun(parameter)

    image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image1.bmp');
    [h, w, ~] = size(image);
    image_original = rgb2gray(image(1:h-mod(h,16), 1:w-mod(w,16), :));
%     image_original = image(1:h-mod(h,16), 1:w-mod(w,16), :);
    image = wdenoise2(image_original, 'DenoisingMethod', 'SURE');
    image(image<0) = 0; image(image>255) = 255;

    [A,H,V,D] = swt2(image,4,'haar');
    cutoff = my_iswt2_second(A,H,V,D, 'haar');
    my_sigma = cutoff./3;
    g = [1 1 1 1].*[parameter parameter+1 parameter+0.5 parameter].* my_sigma .*2.5;
    
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
    enhanced(enhanced<0) = 0; enhanced(enhanced>255) = 255;
    [a, b, c] = aqindex(enhanced,8,6,0,'degree','gray','common')

%     result = -1.*entropy(uint8(enhanced))- ssim(uint8(enhanced),uint8(image));
    disp(['entropy: ' num2str(entropy(uint8(enhanced))) ', SSMI: ' num2str(ssim(uint8(enhanced),uint8(image)))])
%     disp(['WECE_AIQ_original: ' num2str(WECE(image, 2, 4))...
%         ', WECE_AIQ_enhanced: ' num2str(WECE(enhanced, 2, 4)) ...
%         ', Re´nyi-AIQ: ' 'sda'])
    imshow(uint8(enhanced), [0 255])
    title(['Parameter = ' num2str(parameter)])
    waitforbuttonpress;
end




function result = WECE(image, k, n)
    
   result = 0;
   image_sorted = sort(image(:));
   m = size(image_sorted, 1);

   for i = 1:m-1
       for j = 0:n
           term = ((-1).^j) .* nchoosek(n, j) .*((image_sorted(i+1).^2 - image_sorted(i).^2)./2) .*...
                 (i./m).^(k) .*(log2(i).^(j)).*(log2(m).^(n-j));
            result = term + result;
       end
   end
   result = (k.^(n+1))./factorial(n) .* result;

end




