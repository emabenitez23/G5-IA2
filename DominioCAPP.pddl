(define (domain capp)
(:requirements :equality :strips)
(:predicates
	(orientacion ?o)
	(feature ?f)
    (tipo ?t)
    (operacion ?op)
    (feature-tipo ?f ?feat-tipo)
    (orientacion-pieza ?o)
    (orientacion-feature ?f ?o)
    (fabricable ?feat-tipo ?operacion)
    (fabricada ?feat)
 	(en ?p ?maq)
 	(pieza ?p)
 	(maquina ?maq)
 	(herramienta ?herr)
) 

(:action cambio-orientacion-pieza
 :parameters ( ?orientacion-inicial ?orientacion-final )
 :precondition
	(and 
        (orientacion-pieza ?orientacion-inicial) 
        (orientacion ?orientacion-inicial) 
        (orientacion ?orientacion-final)
    )
 :effect
	(and 
		(orientacion-pieza ?orientacion-final)
		(not (orientacion-pieza ?orientacion-inicial))
	)
)

(:action cambio-maquina
 :parameters ( ?maquina-inicial ?maquina-final ?pieza )
 :precondition
	(and 
     	(en ?pieza ?maquina-inicial)
        (pieza ?pieza) 
        (maquina ?maquina-inicial) 
        (maquina ?maquina-final)
    )
 :effect
	(and 
		(en ?pieza ?maquina-final)
		(not (en ?pieza ?maquina-inicial))
	)
)
  
(:action cambio-herramienta-en
 :parameters ( ?maq ?herramienta-inicial ?herramienta-final )
 :precondition
	(and 
     	(en ?herramienta-inicial ?maq)
        (herramienta ?herramienta-inicial)
     	(herramienta ?herramienta-final)
        (maquina ?maq)
     	(= ?maq maquina-fresa)
    )
 :effect
	(and 
		(en ?herramienta-final ?maq)
		(not (en ?herramienta-inicial ?maq))
	)
)
  
(:action operacion_1
 :parameters ( ?oper ?f ?ft ?o ?pieza ?maq ?herr )
 :precondition
	(and 
     	(en ?pieza ?maq)
     	(en ?herr ?maq)
     	(pieza ?pieza)
     	(maquina ?maq)
     	(herramienta ?herr)
     	(= ?maq maquina-fresa)
     	(= ?herr herramienta-fresa)
        (orientacion-pieza ?o)
        (orientacion-feature ?f ?o)
        (orientacion ?o) 
        (feature ?f)
        (tipo ?ft)
        (feature-tipo ?f ?ft)
        (fabricable ?ft ?oper)
        (operacion ?oper)
        (= ?oper fresado-igual-dir)
    )
 :effect
    (fabricada ?f)
)
  
(:action operacion_2
 :parameters ( ?oper ?f ?ft ?o1 ?o2 ?pieza ?maq ?herr)
 :precondition
	(and 
     	(en ?pieza ?maq)
     	(en ?herr ?maq)
     	(herramienta ?herr)
    	(pieza ?pieza)
     	(maquina ?maq)
     	(= ?maq maquina-fresa)
     	(= ?herr herramienta-fresa)
     	(orientacion-pieza ?o1)
        (orientacion-feature ?f ?o2)
        (orientacion ?o1)
     	(orientacion ?o2)
     	(= ?o1 orientacion+y)
        (feature ?f)
        (tipo ?ft)
        (feature-tipo ?f ?ft)
        (fabricable ?ft ?oper)
        (operacion ?oper)
        (= ?oper fresado-dist-dir)
    )
 :effect
    (fabricada ?f)
)

(:action operacion_3
 :parameters ( ?oper ?f ?ft ?o ?pieza ?maq ?herr )
 :precondition
	(and 
     	(en ?pieza ?maq)
     	(en ?herr ?maq)
     	(pieza ?pieza)
     	(maquina ?maq)
     	(herramienta ?herr)
     	(= ?maq maquina-fresa)
     	(= ?herr herramienta-broca)
     	(orientacion-pieza ?o)
        (orientacion-feature ?f ?o)
        (orientacion ?o)
        (feature ?f)
        (tipo ?ft)
        (feature-tipo ?f ?ft)
        (fabricable ?ft ?oper)
        (operacion ?oper)
        (= ?oper taladrado-igual-dir)
    )
 :effect
    (fabricada ?f)
)

(:action operacion_4
 :parameters ( ?oper ?f ?ft ?o1 ?o2 ?pieza ?maq ?herr )
 :precondition
	(and 
     	(en ?pieza ?maq)
     	(en ?herr ?maq)
     	(pieza ?pieza)
     	(maquina ?maq)
     	(herramienta ?herr)
     	(= ?maq maquina-fresa)
     	(= ?herr herramienta-broca)
     	(orientacion-pieza ?o1)
        (orientacion-feature ?f ?o2)
        (orientacion ?o1)
     	(orientacion ?o2)
     	(= ?o1 orientacion+y)
        (feature ?f)
        (tipo ?ft)
        (feature-tipo ?f ?ft)
        (fabricable ?ft ?oper)
        (operacion ?oper)
        (= ?oper taladrado-dist-dir)
    )
 :effect
    (fabricada ?f)
)
  
(:action operacion_5
 :parameters ( ?oper ?f ?ft ?o1 ?o2 ?pieza ?maq ?herr )
 :precondition
	(and 
     	(en ?pieza ?maq)
     	(en ?herr ?maq)
     	(pieza ?pieza)
     	(maquina ?maq)
     	(herramienta ?herr)
     	(= ?maq maquina-torno)
     	(= ?herr herramienta-buril)
        (orientacion-pieza ?o1)
        (orientacion-feature ?f ?o2)
        (orientacion ?o1)
     	(orientacion ?o2)
     	(= ?o1 orientacion+y)
        (feature ?f)
        (tipo ?ft)
        (feature-tipo ?f ?ft)
        (fabricable ?ft ?oper)
        (operacion ?oper)
        (= ?oper torneado)
    )
 :effect
	(fabricada ?f)
)
)
