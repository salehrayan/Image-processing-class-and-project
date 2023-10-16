clc; clear; close all;
format long
A = magic(5);
B = A(1:3,3:4);
C = A(1:5,1);
border = '-------------------------------------------------------';
% disp('row 1 to 3, column 3 to 4:')
% disp(B);
% disp(border);
% disp('row 1 to 5, column 1:')
% disp(C);
% indx = find(A<15);
% disp(A(indx));
D = 0:0.1:10;
E = linspace(0, 10, 101);
isequal(E, D)

