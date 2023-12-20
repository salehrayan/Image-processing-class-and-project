clear; close all;

image_original = imread('pirate.tif');
% image_original = rgb2gray(image_original);
image_original = imresize(image_original, [512 512]);
image_lower_res = imresize(image_original, 1./2, "bicubic");

wt = dddtree2('cplxdt', image_lower_res, 1,'FSfarras','qshift10');


original_data = wt.cfs{1,1};

% Specify the scale factor
scale_factor = 2;

% Get the size of the original data
original_size = size(original_data);

% Initialize an empty array for the upscaled data
upscaled_data = zeros([original_size(1:2) * scale_factor,3,  original_size(4:5)]);

% Loop over the fifth dimension
for i = 1:original_size(5)
    % Loop over the fourth dimension
    for j = 1:original_size(4)
        for k=1:3
        % Extract the 3D slice
            slice = original_data(:, :, k, j, i);
            
            % Upscale using bicubic interpolation
            upscaled_slice = imresize(slice, scale_factor, 'bicubic');
            
            % Assign the upscaled slice to the corresponding position
            upscaled_data(:, :, k, j, i) = upscaled_slice;
        end
    end
end
wt.cfs{1,1} = upscaled_data;

original_data = wt.cfs{1,2};
upscaled_data = zeros([original_size(1:2) * scale_factor,  original_size(4:5)]);
for i=1:2
    for j=1:2
        upscaled_data(:, :, i, j) = imresize(image_lower_res, scale_factor./2, 'bicubic');
    end
end
        
wt.cfs{1,2} = upscaled_data;
imrec = idddtree2(wt);

figure
imshow(image_original, [0 255])

figure
imshow(imresize(image_lower_res, 2, "bicubic"), [0 255])
figure
imshow(imrec, [0 255])


disp(psnr(imresize(image_lower_res, size(image_original), "bicubic"), image_original))
disp(psnr(uint8(round(imrec)), image_original, 255))

disp(snr(double(imresize(image_lower_res, size(image_original), "bicubic")),...
    double(imresize(image_lower_res, size(image_original), "bicubic")-image_original)))
disp(snr(double(round(imrec)), double(round(imrec))-double(image_original)))
