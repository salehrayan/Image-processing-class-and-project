clc;clear; close all;

lb = [100 100 100 100 0.1 0.1 0.1 0.1]';
ub = [300 400 500 600 2 7 7 7]';
rng default
% options = optimoptions('patternsearch', 'Display','iter');
% options = optimoptions('ga', 'Display','iter', 'MaxGenerations',2);
options = optimoptions('particleswarm', 'Display','iter', 'MaxIterations',20, SwarmSize=20);
x = particleswarm(@fun,8, lb, ub,options);
% x = patternsearch(@fun, lb', [], [], [], [], lb, ub, options);
% x = ga(@fun, 8, [], [], [], [], lb, ub,[], options);
% z = MCMA(image, adapthisteq(image));
% x_res1 = [1.0000   18.8615   39.8820   26.5488    0.5699    0.0100    4.7782    2.2178];
% x_res2 = [2.8418   49.9443   46.3454   50.0000    2.0000    0.5000    0.5641    9.0779];
% x_res3 = [2.0049   50.0000   50.0000   10.0000    1.4186    0.5000    1.1803    1.8299];
% x_res4 = [2.6223   20.0000   20.5013   16.1794    1.0238    1.6985    1.9000    3.1941];
% x_res5 = [1.3955   39.6680   40.0000   40.0000    1.0000    0.5000    0.8000    6.0000];
% x_res6 = [1.0000   17.6536   29.2211   10.4791    0.5000    1.6479    2.0205    3.4487];
% x_test = [0.05   20.0000   20.5013   16.1794    8    60   65    70];
% x_res7 = [288.6134  224.1205  200.0000  600.0000    1.5000    5.0000    2.0467    4.1972];
% x_res8 = [285.9771  225.0830  266.7629  575.6981    1.4965    5.0000    1.8322    4.3446];
% x_res9 = [300.0000  246.3768  200.0000  258.5709    1.5000    5.0000    5.0000    5.0000];
% x_res10 = [202.4574  200.0000  200.0000  200.0000    1.5000    5.0000    1.5000    2.4592];
% x_res11 = [200.0000  400.0000  478.6685  600.0000    1.5000    5.0000    5.0000    5.0000];
% x_res12 = [300.0000  400.0000  500.0000  600.0000    1.5000    5.0000    5.0000    5.0000];
% x_res13 = [275.3718  400.0000  500.0000  600.0000    1.5000    4.9918    5.0000    5.0000];
% x_res14 = [300.0000  400.0000  500.0000  600.0000    1.5000    5.0000    5.0000    5.0000];
% x_res15 = [ 284.5020  400.0000  308.8780  206.3742    1.5000    2.5475    4.1608    3.2429];
% x_res16 = [300.0000  265.9039  200.0000  314.2550    1.3668    2.5954    5.0000    5.0000];
% x_res17 = [ 248.5376  209.2343  248.7835  297.4100    1.1908    4.6533    2.4233    4.8344];
% x_res18 = [263.2457  400.0000  500.0000  600.0000    1.5000    5.0000    5.0000    5.0000];
x_res19 = [300.0000  200.0000  228.3887  600.0000    1.5000    5.0000    5.0000    5.0000];
x_res20 = [300.0000  400.0000  213.7833  272.4993    1.5000    5.0000    5.0000    5.0000];
x_res21 = [296.2722  200.0000  234.1062  600.0000    1.5000    5.0000    5.0000    5.0000];
x_res22 = [256.2851  400.0000  499.9983  600.0000    1.5000    5.0000    4.9986    4.9966];
x_res23 = [200.0000  200.0000  290.2083  600.0000    1.5000    5.0000    5.0000    5.0000];
x_res24 = [223.5482  200.0000  397.9944  600.0000    1.5000    5.0000    5.0000    5.0000];

% fun(x_res24)
% cutoff = [300 300 400 500];
% sigmas_test = cutoff./3;
% gains = [1.1 2 3 4] .* sigmas_test .*2.5;
% x_test2 = [cutoff [1.1 2 3 4]];
% fun([100.4884  227.3461  102.0887  182.1730    2.0000    6.7249    7.0000    7.0000])


function result = fun(x)

    image = imread('C:\Users\ASUS\Desktop\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image1.bmp');
    image = rgb2gray(image(1:end, 1:end-2, :));
%     image = image./(max(image, [], 'all'));
    image = wdenoise2(image, 'DenoisingMethod', 'SURE');
    cutoff = x(1:4);
    my_sigma = cutoff./3;
    g = x(5:8) .* my_sigma .*2.5;

    [A,H,V,D] = swt2(image,4,'haar');
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
    result = -1.*MCMA(image, enhanced);
%     result =  -1.*HS(enhanced);
    
end

function result = HS(im)
    [counts,~] = imhist(uint8(im));
    cumulative_sum_image = cumsum(counts)./max(cumsum(counts));
    quartiles = find((abs(cumulative_sum_image-0.75) <0.05)+ (abs(cumulative_sum_image-0.25) <0.05));
    result = (quartiles(end) - quartiles(1))./255;
end

function result = AMBE(image, enhanced)
    result = abs(mean(double(image),"all") - mean(enhanced,"all"));
end

