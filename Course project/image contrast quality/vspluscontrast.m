function  score = vspluscontrast( img,img1)
% vspluscontrast - measure the image quality of distorted image 'dist' with the reference image 'ref'.
% inputs:
% img - the reference image (grayscale image, double type, 0~255)
% img1 - the distorted image (grayscale image, double type, 0~255)
% output:
% score: distortion degree of the distorted image
% This is an implementation of the following algorithm:
% Huizhen Jia, Tonghan Wang,
%"Contrast and visual saliency similarity induced index for Image Quality Assessment"

window           = fspecial('gaussian',2,1.5);
window           = window/sum(sum(window));
Down_step=2;
aveKernel = fspecial('average',2);
aveY1 = conv2(img, aveKernel,'same');
aveY2 = conv2(img1, aveKernel,'same');

img = aveY1(1:Down_step:end,1:Down_step:end);
img1= aveY2(1:Down_step:end,1:Down_step:end);
vs1=spectralResidueSaliency(img);
vs2=spectralResidueSaliency(img1);

mu1= filter2(window,img,'same');
mu2= filter2(window,img1,'same');
mu_sq1                    = mu1.*mu1;
sigma1                    = sqrt(abs(filter2(window,img.*img,'same') - mu_sq1));
mu_sq2                    = mu2.*mu2;
sigma2                    = sqrt(abs(filter2(window,img1.*img1,'same') - mu_sq2));
C1=0.00008;
C2=55;
vs=(2*vs1.*vs2+C1)./(vs1.^2+vs2.^2+C1);
q=(2 * sigma1.*sigma2 + C2) ./ (sigma1.^2 + sigma2.^2 + C2);
score=0.455*(std2(vs))+0.545*(std2(q));


end

function saliencyMap = spectralResidueSaliency(image)
%this function is used to calculate the visual saliency map for the given
%image using the spectral residue method proposed by Xiaodi Hou and Liqing
%Zhang. For more details about this method, you can refer to the paper:
%Saliency detection: a spectral residual approach.

%there are some parameters needed to be adjusted
scale = 0.25; %fixedsc
aveKernelSize =12; %fixed
gauSigma =0.75; %fixed
gauSize =4; %fixed
% scale = 0.25; %fixedsc
% aveKernelSize =3; %fixed
% gauSigma =6; %fixed
% gauSize =15; %fixed

inImg = imresize(image, scale);

%%%% Spectral Residual
myFFT = fft2(inImg);
myLogAmplitude = log(abs(myFFT));
myPhase = angle(myFFT);

mySpectralResidual = myLogAmplitude - imfilter(myLogAmplitude, fspecial('average', aveKernelSize), 'replicate');
saliencyMap = abs(ifft2(exp(mySpectralResidual + 1i*myPhase))).^2;

%%%% After Effect
saliencyMap = mat2gray(imfilter(saliencyMap, fspecial('gaussian', [gauSize, gauSize], gauSigma)));
saliencyMap = imresize(saliencyMap,[size(image,1) size(image,2)]);
end