(define (problem capp-pieza)
    (:domain capp)
    (:objects
     	parte-001
     
        orientacion+x
        orientacion+y
        orientacion+z
        orientacion-x
        orientacion-y
        orientacion-z
     
        s2
        s4
        s6
        s9
        s10
     	h1
     	h3
     	h5
     	h7
     	h9
     	h11
     	h12
     	c1
     
     	cilindrado
        slot
     	step
        through-hole-longitudinal
     	through-hole-transversal
        blind-hole-longitudinal
     	blind-hole-transversal
     
     	torneado
        taladrado-igual-dir
        taladrado-dist-dir
     	fresado-igual-dir
     	fresado-dist-dir
     
     	maquina-fresa
     	maquina-torno
     
     	herramienta-buril
     	herramienta-broca
     	herramienta-fresa
    )
    (:init 
     	(pieza parte-001)
     
        (orientacion orientacion+x)
        (orientacion orientacion+y)
        (orientacion orientacion+z)
        (orientacion orientacion-x)
        (orientacion orientacion-y)
        (orientacion orientacion-z)
     	
     	(feature s2)
     	(feature s4)
     	(feature s6)
     	(feature s9)
     	(feature s10)
     	(feature h1)
     	(feature h3)
     	(feature h5)
     	(feature h7)
     	(feature h9)
     	(feature h11)
     	(feature h12)
     	(feature c1)
     
     	(orientacion-feature s2 orientacion-z)
     	(orientacion-feature s4 orientacion-z)
     	(orientacion-feature s6 orientacion-z)
     	(orientacion-feature s9 orientacion-z)
     	(orientacion-feature s10 orientacion-z)
     	(orientacion-feature h1 orientacion-z)
     	(orientacion-feature h3 orientacion-z)
     	(orientacion-feature h5 orientacion-z)
     	(orientacion-feature h7 orientacion-z)
     	(orientacion-feature h9 orientacion-z)
     	(orientacion-feature h11 orientacion-z)
     	(orientacion-feature h12 orientacion-z)
     	(orientacion-feature c1 orientacion-x)
     	     	
     	(tipo cilindrado)
     	(tipo slot)
     	(tipo step)
     	(tipo through-hole-longitudinal)
     	(tipo through-hole-transversal)
     	(tipo blind-hole-longitudinal)
     	(tipo blind-hole-transversal)
     
     	(feature-tipo s2 step)
     	(feature-tipo s4 step)
     	(feature-tipo s6 step)
     	(feature-tipo s9 slot)
     	(feature-tipo s10 slot)
     	(feature-tipo h1 blind-hole-longitudinal)
     	(feature-tipo h3 through-hole-longitudinal)
     	(feature-tipo h5 through-hole-longitudinal)
     	(feature-tipo h7 through-hole-transversal)
    	(feature-tipo h9 through-hole-transversal)
     	(feature-tipo h11 blind-hole-transversal)
     	(feature-tipo h12 blind-hole-transversal)
     	(feature-tipo c1 cilindrado)
     	
     	(operacion torneado)
     	(operacion taladrado-igual-dir)
     	(operacion taladrado-dist-dir)
     	(operacion fresado-igual-dir)
     	(operacion fresado-dist-dir)
     
     	(fabricable slot fresado-igual-dir)
     	(fabricable step fresado-dist-dir)
     	(fabricable blind-hole-longitudinal fresado-igual-dir)
     	(fabricable blind-hole-transversal fresado-dist-dir)
     	(fabricable through-hole-longitudinal taladrado-igual-dir)
     	(fabricable through-hole-transversal taladrado-dist-dir)
     	(fabricable cilindrado torneado)
     
     	(maquina maquina-fresa)
     	(maquina maquina-torno)
     
     	(herramienta herramienta-buril)
     	(herramienta herramienta-broca)
     	(herramienta herramienta-fresa)
      	
        (orientacion-pieza orientacion-x)
     	(en herramienta-buril maquina-torno)
     	(en herramienta-broca maquina-fresa)
     	(en parte-001 maquina-torno)
    )
    (:goal 
        (and
         	(fabricada c1)
         	(fabricada h5)
         	(fabricada h3)
         	(fabricada h7)
         	(fabricada s2)
         	(fabricada s4)
         	(fabricada s6)
         	(fabricada s9)
         	(fabricada s10)
         	(fabricada h1)
         	(fabricada h9)
         	(fabricada h11)
         	(fabricada h12)
        )
    )
)