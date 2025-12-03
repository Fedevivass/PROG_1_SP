import pygame
from constantes import *
from menu import *
from juego import *
from matriz import *
from terminado import *
from puntuaciones import *

pygame.init()
pygame.display.set_caption(" SUDOKU ")

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True


datos_juego = {"puntuacion":0,"nombre":"","volumen_musica":90,"fila_sel":None,"col_sel":None}

ventana_actual = "menu"
jugadores = {}
while corriendo:
    cola_eventos = pygame.event.get()

    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "jugar":
        ventana_actual = mostrar_juego(pantalla,cola_eventos,matriz_juego,matriz_correcta,datos_juego)
    elif ventana_actual == "niveles":
        pass
    elif ventana_actual == "puntuaciones":
        ventana_actual = mostrar_puntuaciones(pantalla,cola_eventos)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_fin_juego(pantalla,cola_eventos,datos_juego,jugadores)
    if ventana_actual == "salir":
        corriendo = False



    pygame.display.flip()
pygame.quit()