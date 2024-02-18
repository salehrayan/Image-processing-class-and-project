clear; clc; close all;
format long

image = imread('E:\github\Image processing class and project\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\baby.FLT.bmp');
% image = rgb2gray(image);
[h, w, ~] = size(image);
% image = double(imresize(image, [min([h w]) min([h w])], "bicubic"));

[Q, Qn, Rm] = WECE_AQI(image, 8, 6, 0, 'degree', 'gray', 'common');

fprintf('%.10f\n', Q)
fprintf('%.10f\n', Qn)
fprintf('%.10f\n', Rm)


result = WECE([1 1 2 3], 2, 4);





function result = WECE(vorudi, k, n)
    
   result = 0;
   input_sorted = sort(vorudi(:));
   l = size(input_sorted,1);

   for i = 1:(l -1)
       for j = 0:n
           term = ((-1).^j) .* nchoosek(n, j) .*((input_sorted( i+1).^2 - input_sorted( i).^2)./2) .*...
                 (i./l).^(k) .*(log10(i).^(j)).*(log10(l).^(n-j));
            result = term + result;
       end
   end
   result = (k.^(n+1))./factorial(n) .* result;

end

function result = CRTE(vorudi, alpha)

    result = 0;
    input_sorted = sort(vorudi, 2);
    for i=1:8
        result = (1./(alpha-1)).*(1-alpha.*((1-i./8).^(alpha-1)))./8.*input_sorted(:, i)+ result;
    end
end

function Y=orlaon(X,p)

[ro co]=size(X);
Xup=X(1:p,:);
Xup=flipud(Xup);
Xbu=X(ro-p+1:ro,:);
Xbu=flipud(Xbu);
Xp=[Xup;X;Xbu];
Xle=Xp(:,1:p);
Xle=fliplr(Xle);
Xri=Xp(:,co-p+1:co);
Xri=fliplr(Xri);
Y=[Xle Xp Xri];

end

