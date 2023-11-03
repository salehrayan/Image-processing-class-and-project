clc;clear;close all;

I = imread('C:\Users\ASUS\Desktop\Image processing\Horizontal texture features\textures\1.2.12.tiff');
Image = imgaussfilt(I,1, FilterSize=3);

[c, s] = wavedec2(Image,3, 'haar');

[H1 , V1, D1] = detcoef2('all', c, s, 1);
A1 = appcoef2(c,s, 'haar', 1);

[H2 , V2, D2] = detcoef2('all', c, s, 2);
A2 = appcoef2(c,s, 'haar', 2);

[H3 , V3, D3] = detcoef2('all', c, s, 3);
A3 = appcoef2(c,s, 'haar', 3);


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



v1 = wrcoef2("v",c,s,"haar",1);
v2 = wrcoef2("v",c,s,"haar",2);
v3 = wrcoef2("v",c,s,"haar",3);
h1 = wrcoef2("h",c,s,"haar",1);
h2 = wrcoef2("h",c,s,"haar",2);
h3 = wrcoef2("h",c,s,"haar",3);

im = v1+v2+v3;

fig3 = figure;
subplot(2,1,1)
imagesc(I);
colormap gray
title('Original image');

subplot(2,1,2)
imagesc(im);
colormap gray
title('Vertical reconstruction')

fig3.Position = [573, 44, 560, 880];
