L=10;
n=2048;
Fs = n/L;
t=linspace(0,L,n);
% k=(2*pi/L)*[0:n/2-1 -n/2:-1]; ks=fftshift(k);
k = (-n/2: n/2-1)/n *Fs;

S=(3*sin(2*t)+0.5*tanh(0.5*(t-3))+ 0.2*exp(-(t-4).^2)...
+1.5*sin(5*t)+4*cos(3*(t-6).^2))/10+(t/20).^3;
St=fft(S);

figure(1)
subplot(2,1,1) % Time domain
plot(t,S,'k')
set(gca,'Fontsize',14),
xlabel('Time (t)'), ylabel('S(t)')
subplot(2,1,2) % Fourier domain
plot(k,abs(fftshift(St))/max(abs(St)),'k');
axis([-15 15 0 1])
set(gca,'Fontsize',14)
xlabel('frequency (her)'), ylabel('FFT(S)')

figure(2)

width=[10 1 0.2];
for j=1:3
g=exp(-width(j)*(t-4).^2);
subplot(3,1,j)
plot(t,S,'k'), hold on
plot(t,g,'k','Linewidth',2)
set(gca,'Fontsize',14)
ylabel('S(t), g(t)')
end
xlabel('time (t)')


