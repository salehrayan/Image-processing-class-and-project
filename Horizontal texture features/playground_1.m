clc;clear;close all;


wname = 'haar';
[~, psi,xval] = wavefun(wname,8);
plot(xval,psi)
grid on
title(['Approximation of ',wname, ' Wavelet'])