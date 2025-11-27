import pygame
import random
from config import *

def dibujar_texto(pantalla, texto, x, y, color, tamaño):
    fuente = pygame.font.Font(None, tamaño)

    superficie_texto = fuente.render(texto, True, color)

    rectangulo = superficie_texto.get_rect()
    rectangulo.center = (x, y)

    pantalla.blit(superficie_texto, rectangulo)


def dibujar_planilla(pantalla, planilla, puntaje_total):
    MARGEN_X = 50
    MARGEN_Y_INICIAL = 80
    ESPACIO_LINEA = 25
    MITAD_PANTALLA_X = ANCHO_VENTANA // 4
    dibujar_texto(pantalla, "PLANILLA DE PUNTAJES", MITAD_PANTALLA_X, 20, BLANCO, TAMAÑO_FUENTE_NORMAL)

    y = MARGEN_Y_INICIAL

    for categoria, puntos in planilla.items():
        if puntos == None:
            texto_puntos = " - "
        else:
            texto_puntos = str(puntos)
        
        linea_texto = (f"{categoria}: {texto_puntos} ")
        fuente = pygame.font.Font(None, TAMAÑO_FUENTE_CHICA)
        superficie_texto = fuente.render(linea_texto, True, BLANCO)
        pantalla.blit(superficie_texto, (MARGEN_X, y))

        y += ESPACIO_LINEA
    
    dibujar_texto(pantalla, f"PUNTAJE TOTAL: {puntaje_total}", MITAD_PANTALLA_X, y + 20, BLANCO, TAMAÑO_FUENTE_NORMAL)


def dibujar_dados_interactivos(pantalla, dados_valores, dados_bloqueados):
    lista_rects = []
    ESPACIADO = 75
    X_INICIAL = ANCHO_VENTANA - 450
    Y_POSICION = 450

    for i in range(len(dados_valores)):
        valor = dados_valores[i]

        x = X_INICIAL + (i * ESPACIADO)
        y = Y_POSICION

        rect_dado = pygame.Rect(x, y, ANCHO_DADO, ALTO_DADO)

        if dados_bloqueados[i]:
            color_relleno = AMARILLO
        else:
            color_relleno = AZUL_CLARO

        pygame.draw.rect(pantalla, color_relleno, rect_dado, 0)

        dibujar_texto(pantalla, str(valor), rect_dado.centerx, rect_dado.centery, NEGRO, 36)
        lista_rects.append(rect_dado)
    
    return lista_rects

def gestionar_clic(bloqueados_actuales, rects_dados, pos_clic):
    nuevos_bloqueados = list(bloqueados_actuales)

    for x in range(len(rects_dados)):
        rect_dado = rects_dados[x]

        if rect_dado.collidepoint(pos_clic):
            nuevos_bloqueados[x] = not nuevos_bloqueados[x]
            print(f"Dado {x+1} bloqueado: {nuevos_bloqueados[x]}")
            break
    
    return nuevos_bloqueados

def dibujar_boton_tirar(pantalla, tiradas_restantes):

    X_CENTRO = ANCHO_VENTANA - 150
    Y_POSICION = 100

    rect_boton = pygame.Rect(X_CENTRO - 100, Y_POSICION - 25, 200, 50)
    pygame.draw.rect(pantalla, VERDE, rect_boton)

    texto = f"TIRAR ({3- tiradas_restantes})"
    dibujar_texto(pantalla, texto, X_CENTRO, Y_POSICION, BLANCO, TAMAÑO_FUENTE_NORMAL)

    return rect_boton


def manejar_tirada(dados_valores, dados_bloqueados, tiradas_restantes):
    if tiradas_restantes == 0:
        print("Turno terminado. Debe elegir una categoría. ")
        return dados_valores, 0, dados_bloqueados
    
    
    dados_a_mantener = []

    for i in range(len(dados_valores)):
        if dados_bloqueados[i]:
            dados_a_mantener.append(dados_valores[i])
    

    
    dados_finales = list(dados_a_mantener)

    cantidad_a_tirar = 5 - len(dados_a_mantener)

    for x in range(cantidad_a_tirar):
        nuevo_dado = random.randint(1, 6)
        dados_finales.append(nuevo_dado)
    
    nueva_tirada_restante = tiradas_restantes - 1

    return dados_finales, nueva_tirada_restante, [False] * 5


def obtener_rects_planilla(planilla_actual):
    lista_rect_categorias = []

    MARGEN_X = 50
    MARGEN_Y_INICIAL = 80
    ESPACIO_LINEA = 25
    y = MARGEN_Y_INICIAL

    for categoria, puntos in planilla_actual.items():
        if puntos == None:
            rect_categoria = pygame.Rect(MARGEN_X, y, 250, ESPACIO_LINEA)
            lista_rect_categorias.append((categoria, rect_categoria))
        y += ESPACIO_LINEA
    
    return lista_rect_categorias

