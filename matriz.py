from funciones import *
import copy

matriz_correcta = generar_matriz_sudoku()

matriz_juego = copy.deepcopy(matriz_correcta)

colocar_ceros(matriz_juego, 70)