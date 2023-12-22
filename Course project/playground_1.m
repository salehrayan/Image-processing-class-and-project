clc;clear; close all;

image = imread('mandrill.png');
image = rgb2gray(image);


[LoD,HiD,LoR,HiR] = wfilters('haar');


[Lo_col, Hi_col] = local_DEC_FB(image, cat(2, LoD', HiD'), 1);

[Locol_Lorow, Locol_Hirow] = local_DEC_FB(Lo_col, cat(2, LoD', HiD'), 2);
[Hicol_Lorow, Hicol_Hirow] = local_DEC_FB(Hi_col, cat(2, LoD', HiD'), 2);

imshow(Hicol_Lorow, [])


[cA,cH,cV,cD] = dwt2(image,'haar');

figure
imshow(cH, [])


function [Lo,Hi] = local_DEC_FB(X,Df,d)
% 2D Analysis Filter Bank (along one dimension only)
% INPUT:
%    X - NxM matrix,where min(N,M) > 2*length(filter)
%       (N,M are even)
%    Df - analysis filter for the columns
%    Df(:,1) - lowpass filter
%    Df(:,2) - highpass filter
%    d - dimension of filtering (d = 1 or 2)
% OUTPUT:
%     Lo,Hi - lowpass,highpass subbands

lpf = Df(:,1);     % lowpass filter
hpf = Df(:,2);     % highpass filter

if d == 2 , X = X'; end
N = size(X,1);
lf = size(Df,1)/2;
n = 0:N-1;
n = mod(n+lf,N);
X = X(n+1,:);

Lo = dyaddown(conv2(X,lpf),'r',1);
Lo(1:lf,:) = Lo(1:lf,:) + Lo((1:lf)+N/2,:);
Lo = Lo(1:N/2,:);

Hi = dyaddown(conv2(X,hpf),'r',1);
Hi(1:lf,:) = Hi(1:lf,:) + Hi((1:lf)+N/2,:);
Hi = Hi(1:N/2,:);

if d == 2 
    Lo = Lo'; 
    Hi = Hi'; 
end
end