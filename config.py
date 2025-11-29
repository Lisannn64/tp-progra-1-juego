import os
import pygame


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 200, 0)
AZUL_OSCURO = (1, 20, 40)
GRIS_CLARO = (200, 200, 200)
AMARILLO = (255, 255, 0)
AZUL_CLARO = (50, 50, 255)
AMARILLO_LUZ = (255, 255, 100)
VERDE_CLARITO = (150, 255, 150)

ANCHO_VENTANA = 1280
ALTO_VENTANA = 720

ANCHO_DADO = 128
ALTO_DADO= 128

FPS = 30
TITULO_JUEGO = "MINI GENERALA TEMÁTICA - STAR WARS"


TAMAÑO_FUENTE_GRANDE = 60
TAMAÑO_FUENTE_NORMAL = 40
TAMAÑO_FUENTE_CHICA = 30




DADOS_VALORES = [1, 2, 3, 4, 5]
DADOS_BLOQUEADOS = [False, False,False, False, False]
PUNTAJE_TOTAL_SIMULADO = 0
PANTALLA_SIMULADA = {"Maestro Jedi": None, "Sith": None}
RECTS_DADOS = []


CARPETA_ASSETS = "assets"

RUTA_FONDO_MENU = os.path.join(CARPETA_ASSETS, "fondo_menu.png")
RUTA_FONDO_JUEGO = os.path.join(CARPETA_ASSETS, "fondo_juego.png")
RUTA_FONDO_ESTADISTICAS = os.path.join(CARPETA_ASSETS, "fondo_estadisticas.png")
RUTA_FONDO_CREDITOS = os.path.join(CARPETA_ASSETS, "fondo_creditos.png")
RUTA_FONDO_REGLAS = os.path.join(CARPETA_ASSETS, "fondo_reglas.png")
RUTA_FONDO_FINAL = os.path.join(CARPETA_ASSETS, "fondo_final.png")

RUTA_MUSICA_MENU = os.path.join(CARPETA_ASSETS, "musica_ambiente.mp3")
RUTA_MUSICA_JUEGO = os.path.join(CARPETA_ASSETS, "musica_batalla.mp3")
RUTA_SND_HOVER = os.path.join(CARPETA_ASSETS, "hover.mp3")
RUTA_SND_CLICK = os.path.join(CARPETA_ASSETS, "click.mp3")
RUTA_SND_TIRAR = os.path.join(CARPETA_ASSETS, "dados.mp3")
RUTA_SND_ANOTAR = os.path.join(CARPETA_ASSETS, "anotar.mp3")


NOMBRES_DADOS = [
    "fondo_dado1.png", 
    "fondo_dado2.png", 
    "fondo_dado3.png", 
    "fondo_dado4.png", 
    "fondo_dado5.png", 
    "fondo_dado6.png"
]

