import pygame 
from funciones import *
from matriz import *
from constantes import *

pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

boton_volver = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\boton_atras.png",50,40,5,10)
boton_listo = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\boton_listo.png",100,90,200,600)
boton_reset = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\boton_reset.png",100,90,100,600)


def mostrar_juego(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], matriz_juego:list,matriz_correcta:list,datos_juego:dict) -> str:
    retorno = "jugar"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x = evento.pos[0]
            y = evento.pos[1]

            x_rel = x - 10
            y_rel = y - 50

            fila = y_rel // 50
            col  = x_rel // 50
            if 0 <= fila < 9 and 0 <= col < 9:
                datos_juego["fila_sel"] = fila
                datos_juego["col_sel"] = col
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    retorno = "menu"
                if boton_listo["rectangulo"].collidepoint(evento.pos):
                    verificar_sudoku(matriz_juego,matriz_correcta,datos_juego)
                    if datos_juego["puntuacion"] > 100 :
                        retorno = "terminado"
                if boton_reset["rectangulo"].collidepoint(evento.pos):
                    datos_juego["puntuacion"] = 0
                    for i in range(9):
                        for j in range(9):
                            matriz_juego[i][j] = matriz_correcta[i][j]
                    colocar_ceros(matriz_juego, 76)

                    datos_juego["fila_sel"] = None
                    datos_juego["col_sel"] = None

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
                verificar_sudoku(matriz_juego, matriz_correcta, datos_juego)
                if datos_juego["puntuacion"] > 100 or datos_juego["puntuacion"] < -100:
                    retorno = "terminado"
            if evento.key == pygame.K_r:
                datos_juego["puntuacion"] = 0
                for i in range(9):
                    for j in range(9):
                        matriz_juego[i][j] = matriz_correcta[i][j]
                colocar_ceros(matriz_juego, 76)

                datos_juego["fila_sel"] = None
                datos_juego["col_sel"] = None

    dibujar_juego(pantalla,matriz_juego,fondo_pantalla)



    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    pantalla.blit(boton_listo["superficie"],boton_listo["rectangulo"])
    pantalla.blit(boton_reset["superficie"],boton_reset["rectangulo"])

    puntaje_formateado = str(datos_juego["puntuacion"]).zfill(4)

    mostrar_texto(pantalla,f"Puntuacion: {puntaje_formateado}",(100, 10),FUENTE_TEXTO,COLOR_NEGRO)
    


    return retorno
