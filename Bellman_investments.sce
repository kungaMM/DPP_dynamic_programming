// Решение задачи распределения инвестиций
// методом динамического программирования.
clear, clc, mode(0), lines(0,90)
y_1 = 5;
C = [
0 0 0 0
1 3 1 2
-%inf 5 2 -%inf ];
R = [
0 0 0 0
3 5 4 3
-%inf 9 6 -%inf ];
[x9,n] = size(C); // x9 - Количество управлений
y9 = y_1 + 1; // y9=y_1 +1 - Количество состояний
// Вычисляем таблицы для
// динамического программирования - ДП
X = -%inf * ones(y9, n+1);
F = X;
F(:,n+1) = zeros(y9, 1); // что находится сейчас в F ?
for j = n : -1 :1
Fyx = -%inf * ones(y9, x9);
for y = 0 : y_1 // y - состояние на шаге j
for x = 1 : x9 // x - управление на шаге j
yy = y - C(x,j);
if 0 <= yy & yy <= y_1
// Уравнение Ричарда Беллмана
Fyx(1+y,x) = R(x,j) + F(1+y-C(x,j), j+1);
// Fyx(1+ y,x) = R(x,j) + F(1+ yy, j+1);
end
end
end
// F,Fyx
[cFy, cX] = max(Fyx, 'c'); // c - column (столбец)
F(:,j) = cFy;
X(:,j) = cX;
// Печать шапки
xmaxi = sum(bool2s(R(:,j) > -%inf));
write(6, ' ')
write(6, ' Этап ' + string(j)' )
// tire40 = '~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~';
tire40 = part('~', ones(1,20)) + '|' + ...
part('~', ones(1, 6*xmaxi ));
write(6, tire40);
write(6, ' Y' + string(j) + ' Fj(Yj) Xj* | Fyx ');
write(6, tire40);
// Печать только нужных строчек и столбцов таблицы
// Допустимые состояния на этапе j меняются
// в пределах от ymini до ymaxi включительно
ymini = sum(C(1, j:$));
ymaxi = y_1 - sum(C(1, 1: j-1));
Table = [(0 : y_1)', F(:,j), X(:,j), Fyx];
write(6, Table(1+ (ymini:ymaxi), 1:(3+xmaxi)), ...
'( 3(i4,2x), "" | "", 100(i4,2x) )' )
write(6, tire40);
end
// Вычисление fopt, rXopt и rYopt
// ==============================
rXopt = zeros(1, n); // r - row (строка)
rYopt = zeros(1, n);
y = y_1;
for j = 1 : n
rXopt(j) = X(1+ y, j);
rYopt(j) = y;
y = y - C(rXopt(j), j);
end
// Печать ответа:
// ==============
C, R, y_1
write(6,' =========== Ответ: ============')
write(6,' ===============================')
fopt = F(1+y_1, 1);
write(6,' fopt = ' + string(fopt));
write(6, rXopt, '( "" rXopt ="", 100i6 )' )
write(6, rYopt, '( "" rYopt ="", 100i6 )' )
