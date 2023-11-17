clc;clear;close all;


x = [0 -10:10];


fourier_x = fft(x,1000000);
% stem(x)
figure
plot(20.*log10(abs(fourier_x)./1000000))
% stem(angle(fourier_x))
% ylim([-120 -20])
% angle(fourier_x)
% real(fourier_x)
figure
freqz(x, 1000000, 'whole')