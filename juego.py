import pygame 
from funciones import *
from matriz import *
from constantes import *

pygame.init()


def mostrar_juego(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], matriz_juego:list,matriz_correcta,datos_juego:dict) -> str:
    retorno = "jugar"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x = evento.pos[0]
            y = evento.pos[1]
            fila = y // 100
            col = x // 100
            if 0 <= fila < 9 and 0 <= col < 9:
                datos_juego["fila_sel"] = fila
                datos_juego["col_sel"] = col
        if evento.type == pygame.KEYDOWN:
            fila = datos_juego["fila_sel"]
            col = datos_juego["col_sel"]

            if fila is not None and col is not None:
                if pygame.K_1 <= evento.key <= pygame.K_9:
                    numero = evento.key - pygame.K_0
                    matriz_juego[fila][col] = numero
                if evento.key == pygame.K_BACKSPACE:
                    matriz_juego[fila][col] = 0
                if evento.key == pygame.K_RETURN:
                    pass

    dibujar_juego(pantalla,matriz_juego)

    return retorno
