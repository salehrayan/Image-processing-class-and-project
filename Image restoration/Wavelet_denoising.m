clc;clear;close all;

I = imread('C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.4.03.tiff');
std = 40;
shape = size(I);

blur_kernel = [1 1 1 1
    1 1 1 1
    1 1 1 1]/16;
Image = conv2(I, blur_kernel, "same");
Image = Image + std.*randn([shape(1) shape(2)]);

[c, s] = wavedec2(Image,6, 'db5');

[H1 , V1, D1] = detcoef2('all', c, s, 1);
A1 = appcoef2(c,s, 'db5', 1);

[H2 , V2, D2] = detcoef2('all', c, s, 2);
A2 = appcoef2(c,s, 'db5', 2);

[H3 , V3, D3] = detcoef2('all', c, s, 3);
A3 = appcoef2(c,s, 'db5', 3);


fig1 = figure;

subplot(2,2,1)
imagesc(A1);
title('Approximation Coef. of level 1')
colormap gray

subplot(2,2,2)
imagesc(H1)
title('Horizontal Detail Coef. of Level 1')


subplot(2,2,3)
imagesc(V1)
title('Vertical Detail Coef. of Level 1')


subplot(2,2,4)
imagesc(D1)
title('Diagonal Detail Coef. of Level 1')

fig1.Position = [273, 244, 860, 720];


fig2 = figure;

subplot(2,2,1)
imagesc(A2);
title('Approximation Coef. of level 2')
colormap gray

subplot(2,2,2)
imagesc(H2)
title('Horizontal Detail Coef. of Level 2')


subplot(2,2,3)
imagesc(V2)
title('Vertical Detail Coef. of Level 2')


subplot(2,2,4)
imagesc(D2)
title('Diagonal Detail Coef. of Level 2')

fig2.Position = [473, 244, 860, 720];


fig3 = figure;

subplot(2,2,1)
imagesc(A3);
title('Approximation Coef. of level 3')
colormap gray

subplot(2,2,2)
imagesc(H3)
title('Horizontal Detail Coef. of Level 3')


subplot(2,2,3)
imagesc(V3)
title('Vertical Detail Coef. of Level 3')


subplot(2,2,4)
imagesc(D3)
title('Diagonal Detail Coef. of Level 3')

fig3.Position = [573, 244, 860, 720];

had = std.^2 .*sqrt(2.*log2(shape(1).*shape(2)))/115;
c_temp = c(1, (s(1,1)*s(1,2))+1:end);
c_temp(abs(c_temp)<had) = 0;
c(1, (s(1,1)*s(1,2))+1:end) = c_temp;

x = waverec2(c, s, 'db5');

fig4 = figure;
colormap gray
fig4.Position = [0, 100, 600, 600];
imagesc(I)
title("Original image")

fig5 = figure;
colormap gray
fig5.Position = [550, 100, 600, 600];
imagesc(Image)
title("Degraded image")

fig6 = figure;
colormap gray
fig6.Position = [1150, 100, 600, 600];
imagesc(x)
title("Denoised Image")