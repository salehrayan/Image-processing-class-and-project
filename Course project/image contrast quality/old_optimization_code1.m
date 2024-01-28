clc;clear;close all;

lb = [200 200 200 200 0.1 1 1.5 2]';
ub = [300 400 500 600 1.5 5 5 5]';
rng default
options = optimoptions('particleswarm', 'Display','iter', 'MaxIterations',3);
% x = particleswarm(@fun,8, lb, ub,options);
% z = MCMA(image, adapthisteq(image));
% x_res1 = [1.0000   18.8615   39.8820   26.5488    0.5699    0.0100    4.7782    2.2178];
% x_res2 = [2.8418   49.9443   46.3454   50.0000    2.0000    0.5000    0.5641    9.0779];
% x_res3 = [2.0049   50.0000   50.0000   10.0000    1.4186    0.5000    1.1803    1.8299];
% x_res4 = [2.6223   20.0000   20.5013   16.1794    1.0238    1.6985    1.9000    3.1941];
% x_res5 = [1.3955   39.6680   40.0000   40.0000    1.0000    0.5000    0.8000    6.0000];
% x_res6 = [1.0000   17.6536   29.2211   10.4791    0.5000    1.6479    2.0205    3.4487];
% x_test = [0.05   20.0000   20.5013   16.1794    8    60   65    70];
x_res7 = [288.6134  224.1205  200.0000  600.0000    1.5000    5.0000    2.0467    4.1972];

fun(x_res7)
% cutoff = [300 300 400 500];
% sigmas_test = cutoff./3;
% gains = [1.1 2 3 4] .* sigmas_test .*2.5;
% x_test2 = [cutoff [1.1 2 3 4]];
% fun(x_test2)


function result = fun(x)

    image = imread('C:\Users\ASUS\Desktop\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image1.bmp');
    image = rgb2gray(image(1:end, 1:end-2, :));
%     image = image./(max(image, [], 'all'));
    cutoff = x(1:4);
    my_sigma = cutoff./3;
    g = x(5:8) .* my_sigma .*2.5;

    [A,H,V,D] = swt2(image,4,'haar');
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
    result = -1.*MCMA(image, enhanced);
    
end




