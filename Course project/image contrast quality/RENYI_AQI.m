function [Q,Qn,Rm]=RENYI_AQI(X,N,nod,firstangle,angleunits,mode,average)
% [Q,Qn,Rm]=aqindex(X,N,nod,firstangle,angleunits,mode)
% Blind Anistropic Quality Index (AQI). 
% Details can be found in: S. Gabarda and G. Cristóbal, “Blind Image 
% quality assessment through anisotropy”, Journal of the Optical Society 
% of America, Vol. 24, No. 12, 2007, pp. B42-B51.
% This measure discriminates sharp noise free images from distorted images
% Inputs:
% X: color or gray-scale image as double precission matrix
% N: window size in pixels (2, 4, 6, 8, ...) (even number)
% nod: number of directions (1, 2, 3, ...)
% firstangle: set the first orientation in degrees or radians. 
% angleunits: 'degree' or 'radian'
% mode: 'gray' or 'color'
% average: use 'common' for regular average, 'zerofree' to ignore
% zeros in the distribution and 'jpeg' for JPEG correction
% Outputs: 
% (Note that Q and Qn are single or multiple upon solutions are selected
% for gray or color images with the mode option
% Q: AQI
% Qn: normalized AQI
% Rm: expected value of directional image entropy

% By Salvador Gabarda
% Matlab version 7.7 (R2008b)
% toolbox     :  \map\maputils\rad2deg.m
% toolbox     :  \stats\moment.m
% Last updated: 06NOV2015
% salvador.gabarda@gmail.com

[ro co la]=size(X);
angleerror=0;

switch mode
    case 'gray'
        X=round(sum(X,3)./la);
    case 'color'
        % no action
end

[ro co la]=size(X);
        
if isequal(angleunits,'radian')
        firstangle=rad2deg(firstangle);
    elseif isequal(angleunits,'degree')
        % no action taken
    else
        disp('unknown unit')
        angleerror=1;
end

dang=180/nod;
output=0;

for k=1:nod
    if angleerror==1
        break
    end
    ang=(k-1)*dang;
    
    for q=1:la
        Y=orlaon(X(:,:,q),N/2);
        W=localwigner(Y,N,firstangle+ang,'degree');
        R=renyientropy(W);
        R=orlaoff(R,N/2);
        
        % image entropy
        switch average
            case 'common'
            r=R(:); 
            case 'zerofree' % useful with quantization noise
            II=find(R~=0);
            r=R(II);
            case 'jpeg'
            r=R(:);     
            % JPEG correction
            Z1(k,q)=mean(r);
            I=find(r==0);
            if isempty(I)
                Z2(k,q)=0;
            else
                [roI coI]=size(I);
                Z2(k,q)=roI;
            end
        end
        
        
        
        % global image entropy direction k, channel q
        alternative='zero';
        switch alternative
            case 'zero' % first option
                global_im_entropy(k,q)=mean(r);
            case 'two'
                global_im_entropy(k,q)=moment(r(:),2); 
            case 'three'
                global_im_entropy(k,q)=moment(r(:),3); 
            case 'four'
                global_im_entropy(k,q)=moment(r(:),4);
            
        end
    end
    
end


switch average
    case 'common'
        % Quality (raw value)
        Q=std(global_im_entropy,1);
    case 'zerofree'
        Q=std(global_im_entropy,1);
    case 'jpeg'
        % JPEG correction
        SZ2=sum(Z2(:));
        SZ3=(SZ2/(ro*co*nod))^0.1;
        Q=std(global_im_entropy,1)*(1-SZ3); %corrected standard deviation 
end
        
% normalized quality
Rm=mean(global_im_entropy,1); 
Qn=Q./Rm;  


       

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

function Y=orlaoff(X,n)

[ro co]=size(X);
Y=X(n+1:ro-n,n+1:co-n);

end



function result = WECE(image, k, n)
    
   result = 0;
   image_sorted = sort(image(:));
   m = size(image_sorted, 1);

   for i = 1:m-1
       for j = 0:n
           
            result = ((-1).^j) .* nchoosek(n, j) .*((image_sorted(i+1).^2 - image_sorted(i).^2)./2) .*...
                 (i./m).^(k) .*(log2(i).^(j)).*(log2(m).^(n-j)) + result;
       end
   end
   result = (k.^(n+1))./factorial(n) .* result;

end

   

   