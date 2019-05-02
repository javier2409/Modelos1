var vip >= 0; #entradas que se venden en VIP
var grl >= 0; #entradas que se venden en General
var s_vip >= 0;
var s_grl >= 0; #guardias de seguridad que se contratan vip y gral respectivamente

maximize Z: (vip-100)*1500 + grl*800 - (s_vip+s_grl)*700;

s.t. minimo_vip: vip >= 100;
s.t. minimo_grl: grl >= 500;

s.t. limite_espacio: vip + grl*0.5 <= 8000;

s.t. seguridad_vip: 20*s_vip >= vip;
s.t. seguridad_grl: 8*s_grl >= grl;

solve;

printf: "Cantidad de VIP que se venden: %d\n",vip;
printf: "Cantidad de General que se venden: %d\n",grl;
printf: "Cantidad de guardias en VIP: %d\n",s_vip;
printf: "Cantidad de guardias en General: %d\n",s_grl;

end;

