#################################################################
# Nombre      : Entorno                                         #
# Version     : 0.05.03.2017                                    #
# Autor       : Victor Estevez                                  #
# Descripcion : Clase Agentes con Adversarios                   #
##################################################################


from AgenteIA.Agente import Agente
from collections import namedtuple
import time
import math

ElEstado = namedtuple('ElEstado', 'jugador, get_utilidad, tablero, movidas, index')


class AgenteJugador(Agente):

    def __init__(self, altura=1,n=8):
        Agente.__init__(self)
        self.estado = None
        self.juego = None
        self.utilidad = None
        self.tecnica = None
        self.altura = altura

    def jugadas(self, estado):
        raise Exception("Error: No se implemento")

    def get_utilidad(self, estado, jugador):
        raise Exception("Error: No se implemento")

    def testTerminal(self, estado):
        return not self.jugadas(estado)

    def getResultado(self, estado, m):
        raise Exception("Error: No se implemento")

    def minimax(self, estado):

        def valorMax(e, depth):
            if self.testTerminal(e) or depth == 0:
                if self.testTerminal(e):
                    return self.get_utilidad(e, self.estado.jugador)
                elif depth == 0:
                    return self.linear_function(e)  # Replace with actual linear function
            v = -100
            for a in self.jugadas(e):
                v = max(v, valorMin(self.getResultado(e, a), depth - 1))
            return v

        def valorMin(e, depth):
            if self.testTerminal(e) or depth == 0:
                if self.testTerminal(e):
                    return self.get_utilidad(e, self.estado.jugador)
                elif depth == 0:
                    return self.linear_function(e)  # Replace with actual linear function
            v = 100
            for a in self.jugadas(e):
                v = min(v, valorMax(self.getResultado(e, a), depth - 1))
            return v

        return max(self.jugadas(estado), key=lambda a: valorMin(self.getResultado(estado, a), self.altura))

    def expectimax(self, estado):

        def valorMax(e, depth):
            if self.testTerminal(e) or depth == 0:
                if self.testTerminal(e):
                    return self.get_utilidad(e, self.estado.jugador)
                elif depth == 0:
                    return self.linear_function(e)  # Replace with actual linear function
            v = -float('inf')
            for a in self.jugadas(e):
                v = max(v, valorExpectimax(self.getResultado(e, a), depth - 1))
            return v



        def valorExpectimax(e, depth):
            if self.testTerminal(e) or depth == 0:
                if self.testTerminal(e):
                    return self.get_utilidad(e, self.estado.jugador)
                elif depth == 0:
                    return self.linear_function(e)  # Replace with actual linear function
            v = 0
            acciones = self.jugadas(e)
            prob = 1 / len(acciones)
            for a in acciones:
                v += prob * valorMax(self.getResultado(e, a), depth - 1)
            return v

        return max(self.jugadas(estado), key=lambda a: valorExpectimax(self.getResultado(estado, a), self.altura))

    def linear_function(self, estado):
        score = 0
        jugador = self.estado.jugador
        oponente = 'X' if jugador == 'O' else 'O'
        lines, sums = self.get_all_lines(estado.tablero)
        # Iterate through all possible lines in the grid
        for line, k in lines:
            score += self.evaluate_line(line, jugador, oponente) / (1 if sums[k] == 0 else sums[k])

        return score

    def get_all_lines(self, tablero):
        lines = []
        keys = list(tablero.keys())
        size = max(max(k) for k in keys) + 1  # Determine the size of the grid

        if len(keys[0]) == 2:
            # Add all rows and columns for 2D and 3D grids
            for i in range(size):
                lines.append([tablero[(i, j)] for j in range(size) if (i, j) in tablero])
                lines.append([tablero[(j, i)] for j in range(size) if (j, i) in tablero])

            # Add all diagonals for 2D grids
            lines.append([tablero[(i, i)] for i in range(size) if (i, i) in tablero])
            lines.append([tablero[(i, size-1-i)] for i in range(size) if (i, size-1-i) in tablero])
        else:
            sums = []
            for k in range(4):
                sum = 0
                for i in range(size):
                    r1 = [tablero[(i, j, k)] for j in range(size) if (i, j, k) in tablero]
                    r2 = [tablero[(j, i, k)] for j in range(size) if (j, i, k) in tablero]
                    lines.append([r1, k])
                    lines.append([r2, k])
                    sum += len(r1) + len(r2)

                # Add all diagonals for 2D grids
                d1 = [tablero[(i, i, k)] for i in range(size) if (i, i, k) in tablero]
                d2 = [tablero[(i, size-1-i, k)] for i in range(size) if (i, size-1-i, k) in tablero]
                lines.append([d1, k])
                lines.append([d2, k])
                sum += len(d1) + len(d2)
                sums.append(sum)
        return lines, sums
        # If the grid is 3D, add additional lines
        if any(len(k) == 3 for k in keys):
            for i in range(size):
                for j in range(size):
                    lines.append([tablero[(i, j, k)] for k in range(size) if (i, j, k) in tablero])
                    lines.append([tablero[(i, k, j)] for k in range(size) if (i, k, j) in tablero])
                    lines.append([tablero[(k, i, j)] for k in range(size) if (k, i, j) in tablero])

            # Add the main diagonals across the 3D grid
            lines.append([tablero[(i, i, i)] for i in range(size) if (i, i, i) in tablero])
            lines.append([tablero[(i, i, size-1-i)] for i in range(size) if (i, i, size-1-i) in tablero])
            lines.append([tablero[(i, size-1-i, i)] for i in range(size) if (i, size-1-i, i) in tablero])
            lines.append([tablero[(size-1-i, i, i)] for i in range(size) if (size-1-i, i, i) in tablero])

        return lines

    def evaluate_line(self, line: list, jugador, oponente):
        score = (len(line)  - line.count(oponente)) / (len(line) if len(line) > 0 else 1) * line.count(jugador)# Penalize
        return score # Exponential function to increase the score
        score = 0
        if line.count(jugador) == len(line):
            score += 100  # Winning line
        elif line.count(jugador) == len(line) - 1 and line.count(None) == 1:
            score += 10  # Potential winning line
        elif line.count(jugador) == len(line) - 2 and line.count(None) == 2:
            score += 1  # Weak potential winning line

        if line.count(oponente) == len(line):
            score -= 100  # Losing line
        elif line.count(oponente) == len(line) - 1 and line.count(None) == 1:
            score -= 10  # Potential losing line
        elif line.count(oponente) == len(line) - 2 and line.count(None) == 2:
            score -= 1  # Weak potential losing line

        return score
    
    def mide_tiempo(funcion):
        def funcion_medida(*args, **kwards):
            inicio = time.time()
            c = funcion(*args, **kwards)
            print("Tiempo de ejecucion: ", time.time() - inicio)
            return c

        return funcion_medida

    @mide_tiempo
    def programa(self):
            self.set_acciones(self.minimax(self.estado))

