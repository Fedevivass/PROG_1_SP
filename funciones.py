import pygame
import random
import os
import json
from constantes import *

def crear_matriz(cantidad_filas: int, cantidad_columnas: int, valor_inicial: any)->list:
    """
    Crea y devuelve una matriz (lista de listas) de tamaño especificado,
    inicializada con un valor dado.

    Parámetros:
    cantidad_filas : int
        Número de filas que tendrá la matriz.
    cantidad_columnas : int
        Número de columnas que tendrá cada fila de la matriz.
    valor_inicial : any
        Valor con el que se inicializarán todas las posiciones de la matriz.
        Puede ser cualquier tipo de dato (int, str, bool, objeto, etc.).

    Retorna:
    list
        Una lista de listas que representa la matriz creada, donde cada
        elemento es igual a `valor_inicial`.
    """
    matriz = []
    for i in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        matriz += [fila]
    return matriz

def generar_matriz_sudoku():
    """
    Genera una matriz de Sudoku válida de 9x9 siguiendo un patrón base.

    La función crea una grilla estándar de Sudoku utilizando una fila inicial
    del 1 al 9 y aplicando desplazamientos controlados por fila para asegurar
    que no haya repeticiones en filas, columnas ni subcuadrículas 3x3.

    Parámetros
    Ninguno

    Retorna
    list
        Una matriz (lista de listas) de 9x9 que representa un Sudoku completo y válido.
        Cada fila se genera desplazando la fila base mediante un patrón calculado
        según la fila actual (`i`).
    """
    fila_inicial = [1,2,3,4,5,6,7,8,9]
    matriz = []

    for i in range(9):
        if i <= 2:
            desplazamiento = (3 * i) % 9
        elif i <= 5:
            desplazamiento = (3 * i + 1) % 9
        else:
            desplazamiento = (3 * i + 2) % 9

        fila = []
        for j in range(9):
            indice = (j + desplazamiento) % 9
            fila.append(fila_inicial[indice])

        matriz.append(fila)

    return matriz

def colocar_ceros(matriz:list, cantidad_ceros:int)->list:
    """
    Reemplaza una cantidad determinada de posiciones de la matriz por ceros,
    seleccionándolas de forma aleatoria.

    La función recorre la matriz y convierte cada posición (fila, columna)
    en un índice lineal. Luego mezcla aleatoriamente todas las posiciones
    posibles y coloca ceros en las primeras `cantidad_ceros` posiciones
    obtenidas.

    Parámetros
    matriz : list
        Matriz bidimensional (lista de listas) donde se colocarán ceros.
        Se espera que sea rectangular y numérica.
    
    cantidad_ceros : int
        Cantidad total de posiciones que se reemplazarán por el valor 0.
        Si el valor es mayor a la cantidad de elementos totales de la matriz,
        solo se reemplazarán tantos como sea posible.

    Retorna
    list
        La misma matriz recibida como parámetro, pero con `cantidad_ceros`
        elementos reemplazados por 0 en posiciones seleccionadas al azar.
    """
    posiciones = []

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            posiciones.append(i * len(matriz[0]) + j)

    random.shuffle(posiciones)

    for i in range(cantidad_ceros):
        fil = posiciones[i] // len(matriz[0])
        col = posiciones[i] % len(matriz[0])
        matriz[fil][col] = 0

    return matriz

def dibujar_juego(pantalla:pygame.Surface, matriz:list, fondo_pantalla):
    """
    Dibuja el tablero de Sudoku en pantalla, incluyendo la cuadrícula,
    los números y el fondo configurado.

    La función renderiza un área donde se ubicará el Sudoku, dibuja las
    celdas individuales, coloca los números correspondientes de la matriz
    y marca las líneas gruesas que separan los subcuadrantes 3x3.

    Parámetros
    pantalla : pygame.Surface
        Superficie principal donde se dibuja todo el contenido del juego.

    matriz : list
        Matriz 9x9 que representa el estado del Sudoku.
        Los valores diferentes de 0 se dibujan como números en pantalla.
        Los ceros se interpretan como celdas vacías.

    fondo_pantalla : pygame.Surface
        Imagen de fondo que se blitea detrás del tablero.

    Retorna
    None
        La función solo dibuja elementos en la superficie y no retorna nada.
    """
    pantalla.blit(fondo_pantalla, (0, 0))

    celda = 50
    margen_x = 10
    margen_y = 50
    tam_total = 9 * celda

    pygame.draw.rect(pantalla, (255, 255, 255), (margen_x, margen_y, tam_total, tam_total))

    for i in range(9):
        for j in range(9):

            x = margen_x + j * celda
            y = margen_y + i * celda

            rect = pygame.Rect(x, y, celda, celda)
            pygame.draw.rect(pantalla, (100, 100, 100), rect, 1)

            if matriz[i][j] != 0:
                texto = FUENTE_TEXTO.render(str(matriz[i][j]), True, COLOR_NEGRO)
                texto_rect = texto.get_rect(center=(x + celda//2, y + celda//2))
                pantalla.blit(texto, texto_rect)

    for j in range(0, 10, 3):
        x = margen_x + j * celda
        pygame.draw.line(pantalla, (0, 0, 0), (x, margen_y), (x, margen_y + tam_total), 4)

    for i in range(0, 10, 3):
        y = margen_y + i * celda
        pygame.draw.line(pantalla, (0, 0, 0), (margen_x, y), (margen_x + tam_total, y), 4)


    for j in range(0, 10, 3):
        x = margen_x + j * celda
        pygame.draw.line(pantalla, (0, 0, 0), (x, margen_y), (x, margen_y + tam_total), 4)

    for i in range(0, 10, 3):
        y = margen_y + i * celda
        pygame.draw.line(pantalla, (0, 0, 0), (margen_x, y), (margen_x + tam_total, y), 4)

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """
    Muestra texto en pantalla con salto de línea automático según el ancho disponible.

    La función divide el texto en palabras y las va renderizando una por una,
    avanzando horizontalmente. Si una palabra no entra en el ancho máximo de la
    superficie, se realiza un salto de línea automáticamente.

    Parámetros
    surface : pygame.Surface
        Superficie donde se dibujará el texto.
    text : str
        Cadena de texto completa que se desea mostrar. Puede incluir saltos de línea.
    pos : tuple
        Posición inicial (x, y) donde comenzará a dibujarse el texto.
    font : pygame.font.Font
        Fuente utilizada para renderizar el texto.
    color : pygame.Color, opcional
        Color del texto. Por defecto es negro.

    Retorna
    None
        La función dibuja sobre la superficie dada pero no retorna ningún valor.
    """
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

def crear_elemento_juego(textura:str, ancho:int, alto:int, pos_x:int, pos_y:int) -> dict:
    """
    Crea un elemento gráfico del juego a partir de una imagen, generando su
    superficie escalada y su rectángulo de colisión/posición.

    La función carga una textura desde un archivo, la escala al tamaño indicado
    y genera un rectángulo (`pygame.Rect`) con la posición y dimensiones dadas.
    El elemento se devuelve como un diccionario para facilitar su manipulación.

    Parámetros
    textura : str
        Ruta del archivo de imagen que se usará como textura del elemento.
    ancho : int
        Ancho en píxeles al que se escalará la imagen.
    alto : int
        Alto en píxeles al que se escalará la imagen.
    pos_x : int
        Posición horizontal donde se ubicará el elemento en pantalla.
    pos_y : int
        Posición vertical donde se ubicará el elemento en pantalla.

    Retorna
    dict
        Diccionario con dos claves:
        - "superficie": la imagen cargada y escalada.
        - "rectangulo": un objeto pygame.Rect con la posición y tamaño del elemento.
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x, pos_y, ancho, alto)

    return elemento_juego

def crear_botones_menu() -> list:
    """
    Crea una lista de botones para el menú principal del juego.

    La función genera múltiples botones utilizando `crear_elemento_juego`,
    ubicándolos verticalmente uno debajo del otro. Cada botón utiliza la misma
    textura y el mismo tamaño, pero con posiciones Y incrementadas para formar
    una columna de opciones en el menú.

    Parámetros
    Ninguno

    Retorna
    list
        Lista de diccionarios, donde cada diccionario representa un botón del menú.
        Cada diccionario contiene:
        - "superficie": la imagen del botón escalada.
        - "rectangulo": el área en pantalla que ocupa.
    """
    lista_botones = []
    pos_x = 300
    pos_y = 300

    for i in range(4):
        boton = crear_elemento_juego(r"C:\Users\feder\Desktop\juego progra\textura_pregunta.jpg", ANCHO_BOTON, ALTO_BOTON, pos_x, pos_y)
        pos_y += 80
        lista_botones.append(boton)
    
    return lista_botones

def verificar_sudoku(matriz_juego:list, matriz_correcta:list, matriz_inicial:list, datos_juego:dict):

    for i in range(len(matriz_correcta)):
        for j in range(len(matriz_correcta[0])):

            if matriz_inicial[i][j] == 0:
                if matriz_juego[i][j] == matriz_correcta[i][j]:
                    if matriz_juego[i][j] != 0:
                        datos_juego["puntuacion"] += 1
                elif matriz_juego[i][j] != 0:
                    datos_juego["puntuacion"] -= 1

def limpiar_superficie(elemento_juego:dict, textura:str, ancho:int, alto:int) -> None:
    """
    Restablece la superficie gráfica de un elemento del juego cargando nuevamente
    su textura desde archivo y escalándola al tamaño indicado.

    Esta función se utiliza para "limpiar" o actualizar la apariencia visual
    de un elemento ya existente, reemplazando su superficie por una nueva
    generada a partir de la textura recibida.

    Parámetros
    elemento_juego : dict
        Diccionario que representa un elemento gráfico del juego.
        Debe contener al menos la clave:
        - "superficie": superficie de imagen a reemplazar.
    textura : str
        Ruta del archivo de imagen que se utilizará para regenerar la superficie.
    ancho : int
        Ancho en píxeles al que se escalará la nueva textura.
    alto : int
        Alto en píxeles al que se escalará la nueva textura.

    Retorna
    None
        La función modifica el diccionario `elemento_juego` directamente y no retorna valor.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))

def guardar_puntuacion(jugadores: dict, nombre_archivo: str) -> dict | list:
    """
    Guarda una nueva puntuación (representada como un diccionario) en un archivo JSON que contiene una lista de puntuaciones.

    Parámetros:
    - jugadores (dict): diccionario con los datos de un jugador o una puntuación a agregar.
    - nombre_archivo (str): ruta o nombre del archivo JSON donde se almacenan las puntuaciones.

    Funcionamiento:
    - Verifica si el archivo existe:
        - Si existe, lo abre en modo lectura y carga la lista actual de puntuaciones.
        - Si no existe, crea una lista vacía para almacenar las puntuaciones.
    - Agrega el diccionario `jugadores` al final de la lista.
    - Abre el archivo en modo escritura y guarda la lista actualizada en formato JSON, con indentación para mejor lectura.
    - Retorna la lista actualizada de puntuaciones.

    Retorna:
    - La lista completa de puntuaciones actualizada, que puede estar vacía si se crea por primera vez.
    """
    if os.path.exists(nombre_archivo) == True:
        with open(nombre_archivo, "r") as archivo:
                puntuaciones = json.load(archivo)
    else:
        puntuaciones = []

    puntuaciones.append(jugadores)  
    
    with open(nombre_archivo, "w") as archivo:
        json.dump(puntuaciones, archivo, indent=4)

    return puntuaciones

def reiniciar_estadisticas(datos_juego:dict) -> None:
    """
    Reinicia los valores principales del estado del juego al comenzar
    una nueva partida.

    Parámetros
    datos_juego : dict
        Diccionario que almacena las estadísticas del jugador durante la partida.
        Se espera que tenga al menos las claves:
        - "vidas"
        - "puntuacion"
        - "nombre"
        - "tiempo_restante"

    Retorna
    None
        La función modifica el diccionario `datos_juego` directamente.
    """
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""

def ordenar_listas_diccionarios(lista: list, clave: str, criterio: bool = True) -> None:
    """
    Ordena una lista de diccionarios in-place basándose en el valor asociado a una clave específica.

    Parámetros:
    - lista (list): lista de diccionarios a ordenar.
    - clave (str): clave del diccionario cuyo valor se utilizará para la comparación y ordenamiento.
    - criterio (bool, opcional): determina el sentido del ordenamiento.
        - True para ordenar de menor a mayor (orden ascendente).
        - False para ordenar de mayor a menor (orden descendente).
      Por defecto es True.

    Funcionamiento:
    - Valida que el parámetro 'criterio' sea booleano; si no, lo establece en True.
    - Utiliza un algoritmo de ordenamiento tipo burbuja (doble ciclo for).
    - Compara los valores asociados a la clave especificada en dos diccionarios diferentes.
    - Si el orden es incorrecto según el criterio, intercambia las posiciones de los diccionarios en la lista.
    - Modifica la lista original sin retornar nada (ordenamiento in-place).

    Nota:
    - Si la clave no existe en un diccionario, se considera su valor como 0 para la comparación.
    """
    if type(criterio) != bool:
        criterio = True

    for izq in range(len(lista) - 1):
        for der in range(izq + 1,len(lista)):
            dato_izq = lista[izq].get(clave,0)
            dato_der = lista[der].get(clave,0)
            if (criterio == True and dato_izq > dato_der) or (criterio == False and dato_izq < dato_der):
                aux_izq = lista[izq]
                lista[izq] = lista[der]
                lista[der] = aux_izq

def crear_lista(nombre_archivo:str)->list:
    """
    Carga y devuelve una lista de jugadores almacenada en un archivo JSON.

    Parámetros:
    - nombre_archivo (str): ruta o nombre del archivo JSON que contiene la lista de jugadores.

    Funcionamiento:
    - Abre el archivo en modo lectura.
    - Usa json.load para cargar los datos del archivo, que deben ser una lista.
    - Devuelve la lista cargada.

    Retorna:
    - Una lista con los jugadores almacenados en el archivo JSON.
    """
    with open(nombre_archivo, "r") as archivo:
        lista_jugadores = json.load(archivo)

    return lista_jugadores