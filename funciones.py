import pygame
import random
from constantes import *

def crear_matriz(cantidad_filas: int, cantidad_columnas: int, valor_inicial: any)->list:
    matriz = []
    for i in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        matriz += [fila]
    return matriz

def generar_matriz_sudoku():
    fila_inicial = [1,2,3,4,5,6,7,8,9]
    matriz = []

    for i in range(9):
        if i <= 2:
            desplazamiento = (3 * i) % 9
        elif i <= 5:
            desplazamiento = (3 * i + 1) % 9
        else:
            desplazamiento = (3 * i + 2) % 9

        fila = fila_inicial[desplazamiento:] + fila_inicial[:desplazamiento]
        matriz.append(fila)

    return matriz

def colocar_ceros(matriz:list, cantidad_ceros:int)->list:

    if cantidad_ceros > 81:
        cantidad_ceros = 81

    posiciones = []

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            posiciones.append(i)
            posiciones.append(j)

    random.shuffle(posiciones)

    indice = 0
    for _ in range(cantidad_ceros):
        fil = posiciones[indice]
        col = posiciones[indice + 1]
        matriz[fil][col] = 0
        indice += 2

    return matriz

def mostrar_matriz(matriz: list)->None:
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            print(matriz[i][j], end="\t")
        print()

def dibujar_juego(pantalla:pygame.Surface,matriz:list):
    pantalla.fill(COLOR_BLANCO)

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x = j * 100
            y = i * 100
            rect = pygame.Rect(x, y, 100, 100)
            pygame.draw.rect(pantalla, (100, 100, 100), rect, 2)
            if matriz[i][j] != 0:
                texto = FUENTE_TEXTO.render(str(matriz[i][j]), True, COLOR_NEGRO)
                texto_rect = texto.get_rect(center=(x + 50, y + 50))
                pantalla.blit(texto, texto_rect)

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [line.split(' ') for line in text.splitlines()]

    space = font.size(' ')[0]

    max_width, _ = surface.get_size()

    x, y = pos

    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            if x + word_width >= max_width:
                x = pos[0]
                y += word_height

            surface.blit(word_surface, (x, y))

            x += word_width + space

        x = pos[0]
        y += word_height

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x,pos_y,ancho,alto)
    
    return elemento_juego

def crear_botones_menu() -> list:
    lista_botones = []
    pos_x = 300
    pos_y = 300

    for i in range(4):
        boton = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\textura_pregunta.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    
    return lista_botones

def verificar_sudoku(matriz_juego,matriz_correcta):
    if matriz_juego == matriz_correcta:
        retorno = True
    else:
        retorno = False

    return retorno