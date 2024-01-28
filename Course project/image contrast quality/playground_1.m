clear; clc; close all;

image = imread('E:\Image processing\Course project\Wavelet-Based Local Contrast Enhancement for Satellite, Aerial and Close Range Images\horse.NOZ.bmp');
% image = rgb2gray(image);
[h, w, ~] = size(image);
image = double(imresize(image, [min([h w]) min([h w])], "bicubic"));

NoDs = 6;

for i = 1:NoDs
    angle = 180./NoDs.*(i-1);
    b = symmetric_pixelwise_sequence(image./255, 8, angle, 'degree');
    global_entropy(i) = mean(WECE(b, 2, 4), "all");
end

std(global_entropy)

function result = WECE(vorudi, k, n)
    
   result = 0;
   input_sorted = sort(vorudi, 2);

   for i = 1:7
       for j = 0:n
           term = ((-1).^j) .* nchoosek(n, j) .*((input_sorted(:, i+1).^2 - input_sorted(:, i).^2)./2) .*...
                 (i./8).^(k) .*(log2(i).^(j)).*(log2(8).^(n-j));
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

