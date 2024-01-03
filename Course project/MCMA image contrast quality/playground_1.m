clc;clear;close all;

lb = [1 10 10 10 0.01 0.5 0.5 0.5]';
ub = [20 50 50 50 2 10 10 10]';
options = optimoptions('particleswarm', 'Display','final', 'MaxIterations',2);
x = particleswarm(@fun,8, lb, ub,options);
% z = MCMA(image, adapthisteq(image));
% x_res1 = [1.0000   18.8615   39.8820   26.5488    0.5699    0.0100    4.7782    2.2178];
% fun(x_res1)


function result = fun(x)

    image = imread('C:\Users\ASUS\Desktop\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\image1.bmp');
    image = rgb2gray(image(1:end, 1:end-2, :));
    my_sigma = x(1:4)*1200;
    g = x(5:8)*40000;

    [A,H,V,D] = swt2(image,4,'haar');
    enhanced = my_iswt2(A,H,V,D, 'haar', my_sigma, g);
    
    result = -1.*MCMA(image, enhanced);
end




