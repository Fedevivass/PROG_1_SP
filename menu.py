import pygame
from constantes import *
from funciones import *

pygame.init()

lista_botones = crear_botones_menu()
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    retorno = "menu"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    if i == BOTON_JUGAR:
                        retorno = "jugar"
                    elif i == BOTON_NIVEL:
                        retorno = "niveles"
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "puntuaciones"
                    elif i == BOTON_SALIR:
                        retorno = "salir"


    pantalla.blit(fondo_pantalla,(0,0))

    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])

    mostrar_texto(lista_botones[BOTON_JUGAR]["superficie"],"JUGAR",(135,10),FUENTE_TEXTO)
    mostrar_texto(lista_botones[BOTON_NIVEL]["superficie"],"NIVELES",(135,10),FUENTE_TEXTO)
    mostrar_texto(lista_botones[BOTON_PUNTUACIONES]["superficie"],"RANKINGS",(135,10),FUENTE_TEXTO)
    mostrar_texto(lista_botones[BOTON_SALIR]["superficie"],"SALIR",(135,10),FUENTE_TEXTO)


    return retorno