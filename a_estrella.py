from queue import PriorityQueue

def h (p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

def algoritmo_A_estrella (f_puntos, p_inicio, p_bahia_carga):
    contador = 0 
    open_set = PriorityQueue()
    open_set.put((0,contador,p_inicio))
    partida = {}
    g_score = {punto:float("inf") for fila in f_puntos for punto in fila}
    g_score [p_inicio] = 0
    f_score = {punto:float("inf") for fila in f_puntos for punto in fila}
    f_score [p_inicio] = h(p_inicio.get_fil_col(),p_bahia_carga.get_fil_col())

    open_set_hash = {p_inicio}

    while not open_set.empty():

        actual = open_set.get()[2]
        open_set_hash.remove(actual)
        actual.actualizar_vecinos(f_puntos)

        if actual==p_bahia_carga:
            break
        for vecinos_n in actual.vecinos:
            temp_g_score = g_score[actual]+1
            if temp_g_score < g_score[vecinos_n]:
                partida [vecinos_n] = actual
                g_score[vecinos_n] = temp_g_score
                f_score[vecinos_n] = temp_g_score + h (vecinos_n.get_fil_col(), p_bahia_carga.get_fil_col())
                if vecinos_n not in open_set_hash:
                    contador+=1
                    open_set.put((f_score[vecinos_n],contador,vecinos_n))
                    open_set_hash.add(vecinos_n)
    return partida