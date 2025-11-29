import pygame
import random
from config import *
from funciones import calcular_puntaje
import os
import copy

def dibujar_texto(pantalla, texto, x, y, color, tamaño):
    fuente = pygame.font.Font(None, tamaño)

    superficie_texto = fuente.render(texto, True, color)

    rectangulo = superficie_texto.get_rect()
    rectangulo.center = (x, y)

    pantalla.blit(superficie_texto, rectangulo)


def dibujar_planilla(pantalla, planilla, puntaje_total, mouse_pos, estado_juego, dados_valores, nivel_dados):
    MARGEN_X = 50
    MARGEN_Y_INICIAL = 80
    ESPACIO_LINEA = 50
    MITAD_PANTALLA_X = ANCHO_VENTANA // 4
    dibujar_texto(pantalla, "PLANILLA DE PUNTAJES", MITAD_PANTALLA_X, 20, BLANCO, TAMAÑO_FUENTE_NORMAL)

    y = MARGEN_Y_INICIAL

    rect_categorias = []

    for categoria, puntos in planilla.items():
        if puntos == None:
            texto = f"{categoria}"
        else:
            texto = f"{categoria} : {puntos} "

        fuente = pygame.font.Font(None, TAMAÑO_FUENTE_GRANDE)
        color_texto = BLANCO

        superficie_temp = fuente.render(texto, True, color_texto)
        rect_texto = superficie_temp.get_rect()

        rect_texto.x = MARGEN_X
        rect_texto.y = y   


        if estado_juego == "ELEGIR_CATEGORIA" and puntos == None:
            if rect_texto.collidepoint(mouse_pos):
                color_texto = AMARILLO

                puntos_posibles = calcular_puntaje(categoria, dados_valores, nivel_dados)

                texto_fantasma = f"(+{puntos_posibles})"
                sup_fantasma = fuente.render(texto_fantasma, True, VERDE_CLARITO)

                pantalla.blit(sup_fantasma, (rect_texto.right + 10, y))

            rect_categorias.append((categoria, rect_texto.copy()))
        
        superficie_final = fuente.render(texto, True, color_texto)
        pantalla.blit(superficie_final, (rect_texto.x, rect_texto.y))


        y += ESPACIO_LINEA
    
    dibujar_texto(pantalla, f"PUNTAJE TOTAL: {puntaje_total}", MITAD_PANTALLA_X, y + 20, BLANCO, TAMAÑO_FUENTE_NORMAL)
    return obtener_rects_planilla(planilla)

def dibujar_dados_interactivos(pantalla, dados_valores, dados_bloqueados, imagenes_dados, nivel):
    lista_rects = []
    ESPACIADO = 140
    
    X_INICIAL = 550
    Y_POSICION = 500
    fuente_guardado = pygame.font.Font(None, 28)
    
    tematica = nivel.get("tematica", [])

    for i in range(len(dados_valores)):
        valor = dados_valores[i]
        x = X_INICIAL + (i * ESPACIADO)
        y = Y_POSICION
        rect_dado = pygame.Rect(x, y, ANCHO_DADO, ALTO_DADO)

        
        if valor in imagenes_dados and imagenes_dados[valor]:
             pantalla.blit(imagenes_dados[valor], (x, y))
        else:
             if dados_bloqueados[i]: color_relleno = AMARILLO
             else: color_relleno = AZUL_CLARO
             pygame.draw.rect(pantalla, color_relleno, rect_dado, 0)
             dibujar_texto(pantalla, str(valor), rect_dado.centerx, rect_dado.centery, NEGRO, 36)

    
        if dados_bloqueados[i]:
            texto_guardado = fuente_guardado.render("GUARDADO", True, BLANCO)
            rect_g = texto_guardado.get_rect(center=(rect_dado.centerx, rect_dado.top -25))
            pantalla.blit(texto_guardado, rect_g)
            pygame.draw.rect(pantalla, AMARILLO, rect_dado, 3)

        
        if valor <= len(tematica):
            nombre_tema = tematica[valor-1]
            dibujar_texto(pantalla, nombre_tema, rect_dado.centerx, rect_dado.bottom + 20, BLANCO, 30)

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

def dibujar_boton_tirar(pantalla, tiradas_restantes, mouse_pos):
    X_CENTRO = ANCHO_VENTANA - 180

    Y_POSICION = 50
    rect_boton = pygame.Rect(X_CENTRO - 100, Y_POSICION - 25, 200, 50)
    
    
    color = VERDE
    if rect_boton.collidepoint(mouse_pos):
        color = VERDE_CLARITO
    
    
    if tiradas_restantes == 0:
        color = GRIS_CLARO

    pygame.draw.rect(pantalla, ROJO, rect_boton, 2)
    pygame.draw.rect(pantalla, color, rect_boton, border_radius=10)
    
    texto = f"TIRAR ({tiradas_restantes})"
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
        else:
            dados_a_mantener.append(random.randint(1, 6))
        
    dados_finales = list(dados_a_mantener)

    cantidad_a_tirar = 5 - len(dados_a_mantener)

    for x in range(cantidad_a_tirar):
        nuevo_dado = random.randint(1, 6)
        dados_finales.append(nuevo_dado)
    
    nueva_tirada_restante = tiradas_restantes - 1

    return dados_finales, nueva_tirada_restante, dados_bloqueados


def obtener_rects_planilla(planilla_actual):
    lista_rect_categorias = []

    MARGEN_X = 50
    MARGEN_Y_INICIAL = 80
    ESPACIO_LINEA = 50
    ALTO_TEXTO = 40
    y = MARGEN_Y_INICIAL

    for categoria, puntos in planilla_actual.items():
        if puntos == None:
            rect_categoria = pygame.Rect(MARGEN_X, y, 400, ESPACIO_LINEA)
            lista_rect_categorias.append((categoria, rect_categoria))
        y += ESPACIO_LINEA
    
    return lista_rect_categorias

def dibujar_pantalla_final(pantalla, puntaje_total, nombre_ingresado, fondo):
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(AZUL_OSCURO)
    
    dibujar_texto(pantalla, "JUEGO TERMINADO!", ANCHO_VENTANA //2, 150, ROJO, 60)
    dibujar_texto(pantalla, f"Punataje Final: {puntaje_total}", ANCHO_VENTANA //2, 250, BLANCO, 50)
    dibujar_texto(pantalla, "Escribí tu nombre y presioná ENTER:", ANCHO_VENTANA // 2, 350, AMARILLO, 30)

    rect_input = pygame.Rect(ANCHO_VENTANA // 2 - 150, 400, 300, 50)
    pygame.draw.rect(pantalla, BLANCO, rect_input, 2)
    dibujar_texto(pantalla, nombre_ingresado, ANCHO_VENTANA // 2, 425, BLANCO, 40)


def dibujar_menu_principal(pantalla, mouse_pos, fondo):
    if fondo:
        pantalla.blit(fondo, (0,0))
    else:
        pantalla.fill(NEGRO)

    dibujar_texto(pantalla, "MINI GENERALA", ANCHO_VENTANA // 2, 80, ROJO, 80)
    dibujar_texto(pantalla, "STAR WARDS", ANCHO_VENTANA // 2, 140, AMARILLO, 50)

    x_centro = ANCHO_VENTANA // 2
    y_inicio = 250
    espaciado = 60
    ancho_btn = 300
    alto_btn = 50

    opciones = [
        ("1- JUGAR", "jugar"),
        ("2- ESTADISTICAS", "estadisticas"),
        ("3- CRÉDITOS", "creditos"),
        ("4- MOSTRAR REGLAS", "reglas"),
        ("5- SALIR", "salir")
    ]
    rects_botones = {}

    for i, (texto, clave) in enumerate(opciones):
        y = y_inicio + i *espaciado
        rect = pygame.Rect(0, 0, ancho_btn, alto_btn)
        rect.center = (x_centro, y)

        if rect.collidepoint(mouse_pos):
            color = AMARILLO
        else:
            color = BLANCO

    
        pygame.draw.rect(pantalla, AZUL_OSCURO, rect) 
        pygame.draw.rect(pantalla, color, rect, 2) 
        
        dibujar_texto(pantalla, texto, x_centro, y, color, 40)
        rects_botones[clave] = rect
    
    return rects_botones


def dibujar_estadisticas(pantalla, lista_puntajes, mouse_pos, fondo):
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(AZUL_OSCURO)
        
    dibujar_texto(pantalla, "MEJORES JUGADORES", ANCHO_VENTANA // 2, 60, AMARILLO, 60)
    
    dibujar_texto(pantalla, "Nombre                 Puntaje", ANCHO_VENTANA // 2, 120, ROJO, 35)

    y_inicial = 180
    alto_fila = 50
    ancho_fila = 700
    x_centro = ANCHO_VENTANA // 2
    y = 140

    for i, jugador in enumerate(lista_puntajes[:10]):
        y = y_inicial + i * alto_fila

        if i % 2 == 0: color_fondo = GRIS_CLARO
        else:
            color_fondo = NEGRO
        
        rect = pygame.Rect(0, 0, ancho_fila, alto_fila)
        rect.center = (x_centro, y)

        pygame.draw.rect(pantalla, color_fondo, rect)
        

        texto = f"{i+1}. {jugador['nombre']} ....... {jugador['puntaje']}"
        dibujar_texto(pantalla, texto, x_centro, y, BLANCO, 32)

    rect_volver = pygame.Rect(0,0, 200, 50)
    rect_volver.center = (ANCHO_VENTANA // 2, ALTO_VENTANA - 60)

    
    if rect_volver.collidepoint(mouse_pos):
        color = ROJO
    else:
        color = BLANCO

    dibujar_texto(pantalla, "VOLVER", rect_volver.centerx, rect_volver.centery, color, 40)
    
    return rect_volver


def dibujar_reglas(pantalla, mouse_pos, nivel_datos, fondo):
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(AZUL_OSCURO)
    dibujar_texto(pantalla, "Reglas de la fuerza", ANCHO_VENTANA // 2, 50, AMARILLO, 50)

    cats= nivel_datos["categorias"]

    fuente_reglas = pygame.font.Font(None, 32)
    x_start = 50
    y = 120
    espaciado = 40


    reglas = [
        "OBJETIVO: Obtener el mayor puntaje posible completando la planilla.\n",
        "CÓMO JUGAR:",
        "1. Tienes 3 TIROS por turno.",
        "2. Haz clic en los dados para GUARDARLOS (se ponen amarillos).",
        "3. Pulsa TIRAR para relanzar los dados no guardados.",
        "4. Al terminar los tiros, haz clic en una categoría para anotar tus puntos.\n",
        "PUNTAJES:",
        f"- NUMÉRICOS (1 al 6): Suman el valor de esos dados.",
        f"- {cats['Escalera']} (20 pts): Una seguidilla (1-2-3-4-5 o 2-3-4-5-6).",
        f"- {cats['Full']} (30 pts): Tres dados iguales + Dos dados iguales.",
        f"- {cats['Poker']} (40 pts): Cuatro dados iguales.",
        f"- {cats['Generala']} (50 pts): Cinco dados iguales.\n",
        "NOTA: Si no logras ninguna combinación, debes elegir una categoría para tacharla (0 pts)."
    ]

    for linea in reglas:
        if "objetivo" in linea or "CÓMO JUGAR" in linea or "PUNTAJES" in linea:
            color = AMARILLO
        else:
            color = BLANCO
        
        superficie = fuente_reglas.render(linea, True, color)
        pantalla.blit(superficie, (x_start, y))
        y += espaciado
    
    rect_volver = pygame.Rect(0, 0, 200, 50)
    rect_volver.center = (ANCHO_VENTANA // 2, ALTO_VENTANA - 50)

    if rect_volver.collidepoint(mouse_pos):
        color = ROJO
    else:
        color = BLANCO

    dibujar_texto(pantalla, "VOLVER", rect_volver.centerx, rect_volver.centery, color, 40)
    return rect_volver





def dibujar_creditos(pantalla, mouse_pos, fondo):
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(AZUL_OSCURO)
    
    dibujar_texto(pantalla, "CRÉDITOS", ANCHO_VENTANA // 2, 50, AMARILLO, 50)

    textos = [
        "Desarrollado por:",
        "Lisandro Nuñez / div 111",
        "",
        "Materia: Programación 1",
        "Año: 2025"
    ]
    
    y = 160
    for linea in textos:
        if "Desarrollado" in linea:
            color = ROJO
        else:
            color = BLANCO
        dibujar_texto(pantalla, linea, ANCHO_VENTANA // 2, y, color, 40)
        y += 50

    rect_volver = pygame.Rect(0, 0, 200, 50)
    rect_volver.center = (ANCHO_VENTANA // 2, ALTO_VENTANA - 80)

    if rect_volver.collidepoint(mouse_pos):
        color = ROJO
    else:
        color = BLANCO

    dibujar_texto(pantalla, "VOLVER", rect_volver.centerx, rect_volver.centery, color, 40)
    return rect_volver


def cargar_recursos():
    recursos = {}

    recursos ["fondos"] = {
        "menu": None,
        "juego": None,
        "estadisticas": None,
        "creditos": None,
        "reglas": None,
        "final": None
    }

    ruta_fondos = {
        "menu": RUTA_FONDO_MENU,
        "juego": RUTA_FONDO_JUEGO,
        "estadisticas": RUTA_FONDO_ESTADISTICAS,
        "creditos": RUTA_FONDO_CREDITOS,
        "reglas": RUTA_FONDO_REGLAS,
        "final": RUTA_FONDO_FINAL
    }


    recursos["sfx"] = {
        "hover": None,
        "click": None,
        "tirar": None,
        "anotar": None
    }

    if os.path.exists(RUTA_SND_HOVER):
        recursos["sfx"]["hover"] = pygame.mixer.Sound(RUTA_SND_HOVER)

    if os.path.exists(RUTA_SND_CLICK):
        recursos["sfx"]["click"] = pygame.mixer.Sound(RUTA_SND_CLICK)

    if os.path.exists(RUTA_SND_TIRAR):
        recursos["sfx"]["tirar"] = pygame.mixer.Sound(RUTA_SND_TIRAR)

    if os.path.exists(RUTA_SND_ANOTAR):
        recursos["sfx"]["anotrar"] = pygame.mixer.Sound(RUTA_SND_ANOTAR)
    
    
    
    for clave, ruta in ruta_fondos.items():
        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert()
            imagen = pygame.transform.scale(imagen, (ANCHO_VENTANA, ALTO_VENTANA))
            recursos["fondos"][clave] = imagen


    recursos["dados"] = {}
    for i, nombre in enumerate(NOMBRES_DADOS):
        ruta = os.path.join(CARPETA_ASSETS, nombre)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            img = pygame.transform.scale(img, (ANCHO_DADO, ALTO_DADO))
            recursos["dados"][i+1] = img
        else:
            recursos["dados"][i+1] = None

        
    recursos["sfx"] = {}
    if os.path.exists(RUTA_SND_CLICK): 
        recursos["sfx"]["click"] = pygame.mixer.Sound(RUTA_SND_CLICK)
    if os.path.exists(RUTA_SND_TIRAR): 
        recursos["sfx"]["tirar"] = pygame.mixer.Sound(RUTA_SND_TIRAR)
    if os.path.exists(RUTA_SND_ANOTAR): 
        recursos["sfx"]["anotar"] = pygame.mixer.Sound(RUTA_SND_ANOTAR)
    if os.path.exists(RUTA_SND_HOVER): 
        recursos["sfx"]["hover"] = pygame.mixer.Sound(RUTA_SND_HOVER)

    recursos["musica_actual"] = None

    return recursos



def reproducir_musica(recursos, ruta, volumen=0.5, loop=-1):
    if recursos["musica_actual"] == ruta:
        return
    
    if not os.path.exists(ruta):
        print("No se encontró la ruta")
        return
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loop)

    recursos["musica_actual"] = ruta