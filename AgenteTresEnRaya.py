from AgenteIA.AgenteJugador import AgenteJugador
from AgenteIA.AgenteJugador import ElEstado
import numpy as np


class AgenteTresEnRaya(AgenteJugador):

    def __init__(self, n=3, altura=1, index = 0):
        AgenteJugador.__init__(self, altura, n)
        self.h = n
        self.v = n
        self.k = n
        self.index = index 

    def jugadas(self, estado):
        return estado.movidas

    def getResultadoCAMBIAR(self, estado, m, index=0):
        if m not in estado.movidas:
            return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                            get_utilidad=self.computa_utilidad(estado.tablero, m, estado.jugador),
                            tablero=estado.tablero, movidas=estado.movidas, index=index)
        tablero = estado.tablero.copy()
        tablero[m] = estado.jugador
        movidas = list(estado.movidas)
        movidas.remove(m)
        return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                        get_utilidad=self.computa_utilidad(tablero, m, estado.jugador),
                        tablero=tablero, movidas=movidas, index=index)

    def getResultado( self, estado, m ):
        if m not in estado.movidas:
            return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                            get_utilidad=self.computa_utilidad3d(estado.tablero, m, estado.jugador)[0],
                            tablero=estado.tablero, movidas=estado.movidas, index=None)
        tablero = estado.tablero.copy()
        tablero[m] = estado.jugador
        movidas = list(estado.movidas)
        movidas.remove(m)
        return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                        get_utilidad=self.computa_utilidad3d(tablero, m, estado.jugador)[0],
                        tablero=tablero, movidas=movidas, index=m) 

    def computa_utilidad3d(self, tablero, m, jugador):
        return self.computa_utilidad(tablero, m, jugador, index=m[-1]), None
        ultilidades = []
        for i in range(4):
            ultilidades.append(self.computa_utilidad(tablero, m, jugador, index=i))
        ganador = np.argmax(ultilidades)
        return max(ultilidades), ganador 
    
    def get_utilidad(self, estado, jugador):
        return estado.get_utilidad if jugador == 'X' else -estado.get_utilidad

    def testTerminal(self, estado):
        return estado.get_utilidad != 0 or len(estado.movidas) == 0
    
    def mostrar(self, estado):
        for i in range(4):
            self.mostrarCAMBIAR(estado, i)
            print("----")
    def mostrarCAMBIAR(self, estado, index=0):
        tablero = estado.tablero
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(tablero.get((x, y, index), '.')+" ", end="")
            print()

    def computa_utilidad(self, tablero, m, jugador, index=0):
        if (self.en_raya(tablero, m, jugador, (0, 1), index=index) or
                self.en_raya(tablero, m, jugador, (1, 0), index=index) or
                self.en_raya(tablero, m, jugador, (1, -1), index=index) or
                self.en_raya(tablero, m, jugador, (1, 1), index=index)):
            return +1 if jugador == 'X' else -1
        else:
            return 0

    def en_raya(self, tablero, m, jugador, delta_x_y, index=0):
        (delta_x, delta_y) = delta_x_y
        x, y, index = m
        n = 0
        while tablero.get((x, y, index)) == jugador:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y, z = m
        while tablero.get((x, y, index)) == jugador:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1
        return n >= self.k
        

