
from collections import namedtuple

from AgenteTresEnRaya import AgenteTresEnRaya, ElEstado
from Tablero import Tablero
from HumanoTresEnRaya import HumanoTresEnRaya

if __name__ == "__main__":
    N = 4
    luis = HumanoTresEnRaya(N)

    juan = AgenteTresEnRaya(N, altura=2)
    juan.tecnica="podaalfabeta"
    tablero = Tablero(N)
    #print(juan.get_all_lines( a.tablero ))
    #print(juan.funcion_evaluacion(a))

    tablero.insertar(luis)
    tablero.insertar(juan)

    
    tablero.run()