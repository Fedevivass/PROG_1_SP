import pygame
from constantes import *
from funciones import *

pygame.init()

boton_volver = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\boton_atras.png",50,40,10,10)

def mostrar_puntuaciones(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    retorno = "puntuaciones"
    
    fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.KEYDOWN:
            retorno = "menu"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    retorno = "menu"
    
    pantalla.blit(fondo_pantalla,(0,0))
    
    lista_jugadores = crear_lista("partida.json")

    ordenar_listas_diccionarios(lista_jugadores,"Puntuacion",False)
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    y = 120
    for i in range(0,len(lista_jugadores)):
        jugador = lista_jugadores[i]
        texto = f"{i + 1}. {jugador['Nombre']} - {jugador['Puntuacion']} pts"
        superficie_texto = FUENTE_RANKING.render(texto, True, COLOR_NEGRO)
        pantalla.blit(superficie_texto, (250, y))
        y += 40

    return retorno
