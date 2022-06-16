inicio():-      writeln('\nSISTEMA DE CONTROL DE LA VALVULA DE SEGURIDAD'),
                repeat,
                writeln('\nComandos disponibles:'), 
                writeln('\n\t1 . Control del espesor y oxidacion de la valvula'),
                writeln('\n\t2 . Control del funcionamiento del piloto'),
                writeln('\n\t3 . Control de la fuga de gas en la union asiento-orificio'),
                writeln('\n\t4 . Fin del programa'),
                write('\nDijite el numero correspondiente a la accion: '), read(X), number(X),
                (
                    member(X,[1,2,3,4]) -> comando(X);
                    writeln('\nComando no valido, vuelva a intentar'), fail
                ).

comando(1):-    (
                   verificar(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra)    
                ), fail.

comando(2):-    (
                    verificar(el_piloto_funciona_bien)
                ), fail.

comando(3):-    (
                   verificar(se_fija_la_fuga_con_la_llave_en_las_juntas)  
                ), fail.

comando(4):-    writeln('\nPrograma finalizado\n'), !.

verificar(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra):-
    estado(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra, si), writeln('\n>> El estado del equipo se informara a la unidad de inspeccion tecnica inmediatamente');
    estado(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra, no), writeln('\n>> El estado del equipo es adecuado');
    estado(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra, desconocido), writeln('\n>> Verificar si el espesor de la valvula es menor que el limite del umbral'),
    (estado(tienen_efectos_de_deslumbramiento_y_oxidacion, no); verificar(tienen_efectos_de_deslumbramiento_y_oxidacion)).

verificar(tienen_efectos_de_deslumbramiento_y_oxidacion):-
    estado(tienen_efectos_de_deslumbramiento_y_oxidacion, si), writeln('\n>> Se requiere coordinacion para renderizar y pintar el equipo');
    estado(tienen_efectos_de_deslumbramiento_y_oxidacion, desconocido), writeln('\n>> Verificar si el cuerpo de la valvula de seguridad, las tuberias y las juntas tienen efectos de deslumbramiento y oxidacion').

verificar(el_piloto_funciona_bien):-
    estado(el_piloto_funciona_bien, si), writeln('\n>> Ajuste la valvula de seguridad de acuerdo con las instrucciones');
    estado(el_piloto_funciona_bien, no), writeln('\n>> Realizar un servicio completo al piloto y reinstalar');
    estado(el_piloto_funciona_bien, desconocido),estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, no), writeln('\n>> Verificar si el piloto funciona bien'),
    (estado(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio, si); verificar(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio));
    estado(el_piloto_funciona_bien, desconocido), estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, si),
    (verificar(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio
)).


verificar(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio):-
    estado(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio, no), writeln('\n>> Reemplace el asiento y el orificio y coloque la valvula de seguridad en el circuito');
    estado(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio, desconocido), writeln('\n>> Verificar si existe una prevencion adecuada de fugas entre el asiento y el orificio'),
    (estado(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad, si); verificar(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad)).



verificar(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad):-
    estado(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad, no), writeln('\n>> Dar mantenimiento al resorte de la valvula de seguridad');
    estado(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad, desconocido), writeln('\n>> Verificar si es bueno el rendimiento y la eficiencia del resorte de la valvula de seguridad'), 
    (estado(estan_bloqueados_los_sensores_de_la_valvula_de_control, no); verificar(estan_bloqueados_los_sensores_de_la_valvula_de_control)).


verificar(estan_bloqueados_los_sensores_de_la_valvula_de_control):-
    estado(estan_bloqueados_los_sensores_de_la_valvula_de_control, si), writeln('\n>> Limpieza y solucion de problemas de las tuberias de deteccion');
    estado(estan_bloqueados_los_sensores_de_la_valvula_de_control, desconocido), writeln('\n>> Verificar si estan bloqueados los sensores de la valvula de control'),
    (estado(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado, no); verificar(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado)).


verificar(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado):-
    estado(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado, si), writeln('\n>> Coloque la valvula de seguridad en posicion "Abierto"');
    estado(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado, desconocido), writeln('\n>> Verificar si el estado de la valvula esta en la posicion "Cerrado"'),
    (estado(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion, no); verificar(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion)).

verificar(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion):- 
    estado(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion, si), writeln('\n>> La funcion de seguridad es apropiada'); 
    estado(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion, desconocido), writeln('\n>> Verificar si funciona correctamente la valvula de alivio con un aumento de presion del estan_bloqueados_los_sensores_de_la_valvula_de_control% superior a la presion de regulacion'),
    (estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, no); verificar(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
)).

verificar(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas):- 
    estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, si), verificar(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio
);
    estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, no), verificar(el_piloto_funciona_bien);
    estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, desconocido), 
    writeln('\n>> Verificar si tiene la valvula de seguridad una evacuacion continua de gases').

verificar(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio):-
    estado(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio
, no), writeln('\n>> Reemplace el asiento y el orificio y coloque la valvula de seguridad en el circuito');
    estado(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio
, si), writeln('\n>> Ajuste la valvula de seguridad de acuerdo con las instrucciones');
    estado(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio
, desconocido), writeln('\n>> Verificar si existe una fuga prevenible entre el asiento y el orificio'),
    (estado(es_efectivo_el_resorte_de_seguridad
, si); verificar(es_efectivo_el_resorte_de_seguridad
)).

verificar(es_efectivo_el_resorte_de_seguridad):-
    estado(es_efectivo_el_resorte_de_seguridad
, no), writeln('\n>> Reemplace el resorte de seguridad en el servicio');
    estado(es_efectivo_el_resorte_de_seguridad
, desconocido), writeln('\n>> Verificar si es efectivo el resorte de seguridad'),
    (estado(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro, no); verificar(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro)).

verificar(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro):-
    estado(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro, si), writeln('\n>> Limpiar y reparar las fallas de las tuberias de deteccion');
    estado(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro, desconocido), writeln('\n>> Verificar si estan obstruidos los conductos del sensor de presion y control'),
    (estado(es_adecuada_la_presion_de_gas_de_la_linea, si); verificar(es_adecuada_la_presion_de_gas_de_la_linea)).

verificar(es_adecuada_la_presion_de_gas_de_la_linea):-
    estado(es_adecuada_la_presion_de_gas_de_la_linea, no), writeln('\n>> Ajuste el regulador de acuerdo con las instrucciones');
    estado(es_adecuada_la_presion_de_gas_de_la_linea, desconocido), writeln('\n>> Verificar si es adecuada la presion de gas de la linea'),
    (estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
, si); verificar(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas
)).

verificar(se_fija_la_fuga_con_la_llave_en_las_juntas):-
    estado(se_fija_la_fuga_con_la_llave_en_las_juntas, si), writeln('\n>> Informe a la unidad de inspeccion tecnica');
    estado(se_fija_la_fuga_con_la_llave_en_las_juntas, no), writeln('\n>> Enviar un informe al departamento de reparacion para solucionar la averia');
    estado(se_fija_la_fuga_con_la_llave_en_las_juntas, desconocido), writeln('\n>> Verificar si se fija la fuga con la llave en las juntas'),
    (estado(hay_una_fuga_de_gas_en_la_junta, si); verificar(hay_una_fuga_de_gas_en_la_junta)).

verificar(hay_una_fuga_de_gas_en_la_junta):-
    estado(hay_una_fuga_de_gas_en_la_junta, no), writeln('\n>> La junta de la valvula de seguridad no tiene fugas de gas.');
    estado(hay_una_fuga_de_gas_en_la_junta, desconocido), writeln('\n>> Verificar si hay una fuga de gas en la junta').


%RAMA IZQUIERDA
estado(es_el_espesor_de_la_valvula_menor_que_el_limite_del_umbra,desconocido).
estado(tienen_efectos_de_deslumbramiento_y_oxidacion,desconocido).

%RAMA CENTRAL
estado(el_piloto_funciona_bien, desconocido).
estado(existe_una_prevencion_adecuada_de_fugas_entre_el_asiento_orificio, desconocido).
estado(es_bueno_el_rendimiento_y_la_eficiencia_del_resorte_de_la_valvula_de_seguridad, desconocido).
estado(estan_bloqueados_los_sensores_de_la_valvula_de_control, desconocido).
estado(esta_el_estado_de_la_valvula_en_la_posicion_Cerrado, desconocido).
estado(estan_bloqueados_los_sensores_de_la_valvula_de_control0_superio__l_presio_d_regulacion, desconocido).
estado(tiene_la_valvula_de_seguridad_una_evacuacion_continua_de_gas, si).
estado(existe_una_fuga_prevenible_entre_el_asiento_y_el_orificio, desconocido).
estado(es_efectivo_el_resorte_de_seguridad, desconocido).
estado(estan_obstruidos_los_tubos_del_sensor_de_presion_y_contro, desconocido).
estado(es_adecuada_la_presion_de_gas_de_la_linea, no).

%RAMA DERECHA
estado(se_fija_la_fuga_con_la_llave_en_las_juntas, desconocido).
estado(hay_una_fuga_de_gas_en_la_junta, desconocido).