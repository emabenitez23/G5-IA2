(define (problem REGISTRO_001) 
	(:domain aviones)
	(:objects 	
		LA01 
		AA02 
		FB03 
		GO01 

		AER 
		BAR 
		LIM 
		MEX 

		CARGA_MERCANCIAS_RESTRINGIDAS
		CARGA_FRAGIL
		CARGA_PERECIBLE
		CARGA_GENERAL
		CARGA_ANIMALES_VIVOS
	)

	(:init
    
    	(avion LA01)
		(avion AA02)
		(avion FB03)
		(avion GO01)
    
    	(aeropuerto AER)
    	(aeropuerto BAR)
    	(aeropuerto LIM)
    	(aeropuerto MEX)

    	(carga CARGA_MERCANCIAS_RESTRINGIDAS)
    	(carga CARGA_FRAGIL)
    	(carga CARGA_PERECIBLE)
    	(carga CARGA_GENERAL)
    	(carga CARGA_ANIMALES_VIVOS)
       
    	(en LA01 AER)   
    	(en AA02 BAR)
    	(en FB03 LIM)
    	(en GO01 MEX)

    	(en CARGA_ANIMALES_VIVOS AER)
    	(en CARGA_PERECIBLE LIM)
    	(en CARGA_GENERAL AER)
    	(en CARGA_FRAGIL BAR)
		(en CARGA_MERCANCIAS_RESTRINGIDAS MEX)    
	)

	(:goal 
    	(and
        	(en CARGA_ANIMALES_VIVOS MEX)
        	(en CARGA_PERECIBLE MEX)
        	(en CARGA_GENERAL BAR)
        	(en CARGA_FRAGIL AER)
        	(en CARGA_MERCANCIAS_RESTRINGIDAS LIM)
		(en FB03 MEX)
         	(en AA02 MEX)
         	(en GO01 LIM)
         	(en LA01 BAR)
    	)
	)
)		
