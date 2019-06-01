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
param goles_jugada{i in Jugadores};
param goles_penal{i in Jugadores};
param goles_visitante{i in Jugadores};
param goles_recibidos_arq{i in Jugadores};
param goles_contra{i in Jugadores};
param veces_figura{i in Jugadores};
param vallas_invictas{i in Jugadores};
param amarillas{i in Jugadores};
param rojas{i in Jugadores};
param penales_errados{i in Jugadores};
param penales_atajados{i in Jugadores};

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
																p15~F15,
																goles_jugada~GJ,
																goles_penal~GP,
																goles_visitante~GV,
																goles_recibidos_arq~GR,
																goles_contra~GC,
																veces_figura~VF,
																vallas_invictas~VI,
																amarillas~TA,
																rojas~TR,
																penales_errados~PE,
																penales_atajados~PA;


var Y{i in Jugadores, j in Partidos} >= 0 binary; #el jugador i forma parte del equipo en la fecha j
var L{i in Jugadores,j in Partidos} >= 0 binary; #el jugador i es capitan en el partido j
var T{i in Jugadores,j in Partidos} >= 0 binary; #el jugador i es titular en el partido j
var C{i in Jugadores, j in Partidos} >= 0; #jugador i comprado en la fecha j
var V{i in Jugadores, j in Partidos} >= 0; #jugador i vendido en la fecha j
var ev{i in Jugadores, j in Partidos: j>1} >= 0; # estaba en la fecha anterior y no fue vendido
var nc{i in Jugadores, j in Partidos: j>1} >= 0; # no estaba en la fecha anterior y fue comprado

maximize Z: sum{i in Jugadores} 
													 	 ((T[i,1]*p1[i])
														+ (T[i,2]*p2[i])
														+ (T[i,3]*p3[i])
														+ (T[i,4]*p4[i])
														+ (T[i,5]*p5[i])
														+ (T[i,6]*p6[i])
														+ (T[i,7]*p7[i])
														+ (T[i,8]*p8[i])
														+ (T[i,9]*p9[i])
														+ (T[i,10]*p10[i])
														+ (T[i,11]*p11[i])
														+ (T[i,12]*p12[i])
														+ (T[i,13]*p13[i])
														+ (T[i,14]*p14[i])
														+ (T[i,15]*p15[i])

													 	+ (L[i,1]*p1[i])
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

s.t. cantidad_total_jugadores{j in Partidos}: sum{i in Jugadores} Y[i,j] = 15;

s.t. cantidad_jugadores_comprados{j in Partidos: j > 1}: sum{i in Jugadores} C[i,j] <= 4;
s.t. cantidad_jugadores_vendidos{j in Partidos: j > 1}: sum{i in Jugadores} V[i,j] <= 4;

s.t. estaba_en_la_fecha_anterior_y_no_fue_vendido{i in Jugadores, j in Partidos: j>1}: 2*ev[i,j] <= Y[i, j-1] + (1 - V[i,j]);
s.t. estaba_en_la_fecha_anterior_y_no_fue_vendido_2{i in Jugadores, j in Partidos: j>1}: ev[i,j] + 1 >= Y[i, j-1] + (1 - V[i,j]);

s.t. no_estaba_en_la_fecha_anterior_y_fue_comprado{i in Jugadores, j in Partidos: j>1}: 2*nc[i,j] <= (1 - Y[i,j-1]) + C[i,j];
s.t. no_estaba_en_la_fecha_anterior_y_fue_comprado2{i in Jugadores, j in Partidos: j>1}: nc[i,j] + 1 >= (1 - Y[i,j-1]) + C[i,j];

s.t. comprado_forma_parte_del_equipo{i in Jugadores, j in Partidos: j>1}: Y[i,j] <= ev[i,j] + nc[i,j];
s.t. comprado_forma_parte_del_equipo_2{i in Jugadores, j in Partidos: j>1}: 2*Y[i,j] >= ev[i,j] + nc[i,j];

s.t. limite_por_club{j in Clubes, p in Partidos}: sum{i in Jugadores: club[i]=j}Y[i,p] <= 3;

s.t. limite_arqueros{j in Partidos}: sum{i in Jugadores:posicion[i] = 'ARQ'} Y[i,j] = 2;
s.t. limite_defensores{j in Partidos}: sum{i in Jugadores:posicion[i] = 'DEF'} Y[i,j] = 4;
s.t. limite_volantes{j in Partidos}: sum{i in Jugadores:posicion[i] = 'VOL'} Y[i,j] = 5;
s.t. limite_delanteros{j in Partidos}: sum{i in Jugadores:posicion[i] = 'DEL'} Y[i,j] = 4;

s.t. capitan_es_del_equipo{i in Jugadores, j in Partidos}: L[i,j] <= Y[i,j];

s.t. titular_es_parte_de_equipo{i in Jugadores, j in Partidos}: T[i,j] <= Y[i,j];

s.t. once_titulares{j in Partidos}: sum{i in Jugadores} T[i,j] = 11;
s.t. un_arquero{j in Partidos}: sum{i in Jugadores: posicion[i]='ARQ'} T[i,j] = 1;
s.t. tres_defensores{j in Partidos}: sum{i in Jugadores: posicion[i]='DEF'} T[i,j] = 3;
s.t. cuatro_volantes{j in Partidos}: sum{i in Jugadores: posicion[i]='VOL'} T[i,j] = 4;
s.t. tres_delanteros{j in Partidos}: sum{i in Jugadores: posicion[i]='DEL'} T[i,j] = 3;

s.t. un_capitan_por_partido{j in Partidos}: sum{i in Jugadores} L[i,j] = 1;
s.t. capitan_es_titular{i in Jugadores, j in Partidos}: L[i,j] <= T[i,j];

s.t. limite_dinero: sum{i in Jugadores, j in Partidos: j=1} (Y[i,j]*Precio[i]) + sum{i in Jugadores, j in Partidos: j > 1} (C[i,j]*Precio[i] - V[i,j]*Precio[i]) <= 65000000;

solve;

for {j in Partidos}{
	printf:'\n';
	printf: "------------Partido %d-------------\n",j;
	printf: '***Titulares:\n';
	for {i in Jugadores: T[i,j]=1}{
		printf: "%s, %s \n",i,posicion[i];
	}
	printf:'\n';
	printf: '***Suplentes: \n';
	for {i in Jugadores: T[i,j]=0 and Y[i,j]=1}{
		printf: "%s, %s \n",i,posicion[i];
	}
	printf:'\n';
	printf: '***Capitan \n';
	for {i in Jugadores: L[i,j]=1}{
		printf: "%s, %s \n",i,posicion[i];
	}
}

printf: "----------Puntos----------\n";
printf: "Puntaje obtenido: %d \n",Z;
end;