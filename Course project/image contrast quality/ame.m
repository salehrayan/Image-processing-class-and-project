
% of the image X of size MxM by using blocks of size LxL

function E=ame(X,L)

%	L=5; 
    sz = size(X);
	how_many_m =floor(sz(1)/L);
    how_many_n =floor(sz(2)/L);
    
	
	E=0.; 
	B1=zeros(L);
	m1=1;
	for m=1:how_many_m
	    n1=1;
	    for n=1:how_many_n
	    	B1=X(m1:m1+L-1,n1:n1+L-1);
            b_min=min(min(B1));
            b_max=max(max(B1));

            if b_min>0 
                b_ratio=(b_max-b_min)/(b_max+b_min);
                E=E+20.*log(b_ratio);	  
            end;

            n1=n1+L;	              
	    end;
	    m1=m1+L;
	end;
	E=-1.*(E/how_many_m)/how_many_n;
