function R=renyientropy(W,alpha)
% R=renyientropy(W,alpha)
% calculates pixelwise WECE entropy from the pseudo-Wigner distribution W 
% produced by "localwigner"
% Inputs:
% W: pseudo-Wigner distribution of a given image by function "localwigner"
% alpha: shape parameter (use a positive integer: 1, 2, 3, ...).
% By omission alpha=3 is used. When alpha=1 the outcome will be 
% the Shannon entropy.
% Outputs:
% R: pixel-wise WECE entropy (or Shannon if alpha=1) of the image
% in the direction given by W


 
% normalize pseudo-Wigner distribution
[ro co N]=size(W);    
W2=reshape(W,ro*co,N);
P=W2.*conj(W2);
S=sum(P,2);
SS=repmat(S,1,N);
P=P./(SS+eps);

if nargin==1
    alpha=3;
end

if alpha==1
    % Rényi entropy = Shannon entropy
    Pp=P.*log2(P+eps);
    Q=-sum(Pp,2);
else
    % WECE entropy
%     P=P.^alpha;
%     Q=(1/(1-alpha))*log2(sum(P,2)+eps);
    Q = WECE(P, 2, 4);
%     Q = CRTE(P, 2);
    R = reshape(Q,ro,co);
end

% round-off error correction
% I=find(Q<0); 
% Q(I)=0;
% II=find(Q>log2(N));
% Q(II)=0;
% U=reshape(Q,ro,co);
% R=U./log2(N);
end
 

function result = WECE(vorudi, k, n)
    
   result = 0;
   input_sorted = sort(vorudi, 2);

   for i = 1:7
       for j = 0:n
           term = ((-1).^j) .* nchoosek(n, j) .*((input_sorted(:, i+1).^2 - input_sorted(:, i).^2)./2) .*...
                 (i./8).^(k) .*(log(i).^(j)).*(log(8).^(n-j));
            result = term + result;
       end
   end
   result = (k.^(n+1))./factorial(n) .* result;

end

function result = CRTE(vorudi, alpha)

    result = 0;
    for i=1:8
        result = (1./(alpha-1)).*(1-alpha.*((1-i./8).^(alpha-1)))./8.*vorudi(:, i);
    end
end






