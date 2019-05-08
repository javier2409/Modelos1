set Jugadores;

set Partidos := {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
set Posiciones := {"ARQ","DEF","VOL","DEL"};
set Clubes := {'Aldosivi de MdP', 'Argentinos Juniors', 'Arsenal FC',
       'Atlético de Rafaela', 'Banfield', 'Belgrano de Cba',
       'Boca Juniors', 'Colón de Santa Fe', 'Crucero del Norte',
       'Defensa y Justicia', 'Estudiantes LP', 'Gimnasia LP',
       'Godoy Cruz AT', 'Huracán', 'Independiente', 'Lanús',
       "Newells Old Boys", 'Nueva Chicago', 'Olimpo de BB', 'Quilmes AC',
       'Racing Club', 'River Plate', 'Rosario Central',
       'San Lorenzo de A', 'San Martín SJ', 'Sarmiento de Junín',
       'Temperley', 'Tigre', 'Unión de Santa Fe', 'Vélez Sarsfield'};


param posicion{i in Jugadores} symbolic in Posiciones;
param club{i in Jugadores} symbolic in Clubes;
param AcT{i in Jugadores};
param p1{i in Jugadores};
param p2{i in Jugadores};
param p3{i in Jugadores};
param p4{i in Jugadores};
param p5{i in Jugadores};
param p6{i in Jugadores};
param p7{i in Jugadores};
param p8{i in Jugadores};
param p9{i in Jugadores};
param p10{i in Jugadores};
param p11{i in Jugadores};
param p12{i in Jugadores};
param p13{i in Jugadores};
param p14{i in Jugadores};
param p15{i in Jugadores};

param Precio{i in Jugadores};
param PuntosTotales{i in Jugadores};

table data IN "CSV" "NoNulos.csv" : Jugadores <- [Jugador], 	posicion~Puesto, 
																Precio~Cotizacion,
																PuntosTotales~AcT,
																club~Equipo,
																p1~F1,
																p2~F2,
																p3~F3,
																p4~F4,
																p5~F5,
																p6~F6,
																p7~F7,
																p8~F8,
																p9~F9,
																p10~F10,
																p11~F11,
																p12~F12,
																p13~F13,
																p14~F14,
																p15~F15;


var Y{i in Jugadores} >= 0 binary;
var L{i in Jugadores,j in Partidos} >= 0 binary;
var T1 >= 0 binary;
var T2 >= 0 binary;
var T3 >= 0 binary;
var T4 >= 0 binary;

maximize Z: sum{i in Jugadores} (Y[i]*PuntosTotales[i] 	+ (L[i,1]*p1[i])
														+ (L[i,2]*p2[i])
														+ (L[i,3]*p3[i])
														+ (L[i,4]*p4[i])
														+ (L[i,5]*p5[i])
														+ (L[i,6]*p6[i])
														+ (L[i,7]*p7[i])
														+ (L[i,8]*p8[i])
														+ (L[i,9]*p9[i])
														+ (L[i,10]*p10[i])
														+ (L[i,11]*p11[i])
														+ (L[i,12]*p12[i])
														+ (L[i,13]*p13[i])
														+ (L[i,14]*p14[i])
														+ (L[i,15]*p15[i]));

s.t. cantidad_jugadores: sum{i in Jugadores} Y[i] = 11;

s.t. limite_club{j in Clubes}: sum{i in Jugadores: club[i]=j}Y[i] <= 3;

s.t. limimte_arqueros: sum{i in Jugadores:posicion[i] = 'ARQ'} Y[i] = 1;
s.t. limite_defensores: sum{i in Jugadores:posicion[i] = 'DEF'} Y[i] = 4*T1 + 4*T2 + 3*T3;
s.t. limite_mediocampistas: sum{i in Jugadores:posicion[i] = 'VOL'} Y[i] = 4*T1 + 3*T2 + 4*T3;
s.t. limite_delanteros: sum{i in Jugadores:posicion[i] = 'DEL'} Y[i] = 2*T1 + 3*T2 + 3*T3;

s.t. solo_una_tactica: T1 + T2 + T3 = 1;

s.t. capitan_es_titular{i in Jugadores, j in Partidos}: L[i,j] <= Y[i];

s.t. un_capitan_por_partido{j in Partidos}: sum{i in Jugadores} L[i,j] = 1;

s.t. limite_dinero: sum{i in Jugadores} Y[i]*Precio[i] <= 58800000;

solve;

printf: "----------Jugadores----------\n";
for {j in Jugadores: Y[j]=1}{
	printf: "%s, %s \n",j,posicion[j];
}

printf: "----------Tactica----------\n";
printf: if T1=1 then "Usando 4-4-2 \n" else "";
printf: if T2=1 then "Usando 4-3-3 \n" else "";
printf: if T3=1 then "Usando 3-4-3 \n" else "";

printf: "----------Capitanes----------\n";
for {p in Partidos,j in Jugadores : L[j,p]=1}{
	printf: "Capitan del partido %d: %s \n",p,j;
}

printf: "----------Puntos----------\n";
printf: "Puntaje obtenido: %d \n",Z;
end;