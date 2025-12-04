from funciones import *
matriz_correcta = generar_matriz_sudoku()

matriz_juego = crear_matriz(9,9,0)
for i in range(len(matriz_correcta)):
    for j in range(len(matriz_correcta[0])):
        matriz_juego[i][j] = matriz_correcta[i][j]

colocar_ceros(matriz_juego, 10)

matriz_inicial = crear_matriz(9,9,0)
for i in range(len(matriz_correcta)):
    for j in range(len(matriz_correcta[0])):
        matriz_inicial[i][j] = matriz_juego[i][j]