x = [-3 -2.5 -2 -1.5 -1 -0.5 0 0.5 1.0 1.5 2 2.5 3];
y = [-0.2 -0.2 0.6 1 0.35 -0.3 0 0.25 -0.4 -1 0.6 0.2 0.2];

xq = -3:0.1:3;

%zadanie 2 - interpolacja dla punktu
p1 = interp1(x,y,0.25)
p2 = interp1(x,y,0.25, 'nearest')
p3 = interp1(x,y,0.25, 'spline')
p4 = interp1(x,y,0.25, 'PCHIP')

% najbliżej wartości z wykresu jest sposób spline

%zadanie 3 - wykres interpolacji
%linear
v1 = interp1(x,y,xq);
plot(xq, v1)
hold on

%nearest
v2 = interp1(x,y,xq, 'nearest');
plot(xq, v2)

%spline
v3 = interp1(x,y,xq, 'spline');
plot(xq, v3)

%cubic
v4 = interp1(x,y,xq, 'PCHIP');
plot(xq, v4)

legend('linear','nearest', 'spline', 'PCHIP');
hold off

%moim zdaniem najskuteczniejsza metodą interpolacji jest metoda spline

%zadanie 4 - polyfit
%udało się odtworzyć mniej więcej za pomoca wielomianu o stopniu 8 
p = polyfit(x, y, 8);
f1 = polyval(p, xq);

figure
plot(x,y,'o')
plot(xq,f1)
hold off

%zadanie 5 - wartość dla wielomianu
p5 = polyval(p, 0.25)

%wartosć jest podobna do tej uzyskane w wyniku interpolacji linear

