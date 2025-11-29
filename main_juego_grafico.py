import pygame
import csv
import os
from config import *
from renderizador import *
from ventana_juego import *
from funciones import *



def obtener_puntaje(jugador):
    return jugador["puntaje"]

def leer_puntajes_csv():
    archivo_nombre = "puntajes.csv"
    lista_puntajes = []
    
    
    if os.path.exists(archivo_nombre):
        with open(archivo_nombre, mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if len(fila) >= 2:
                    nombre = fila[0]
                    puntaje_str = fila[1]
                    if puntaje_str.isdigit():
                        lista_puntajes.append({"nombre": nombre, "puntaje": int(puntaje_str)})
    
    
    lista_puntajes.sort(key=obtener_puntaje)
    lista_puntajes.reverse()
    lista_puntajes = lista_puntajes[:10]
    return lista_puntajes

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("MINI GENERALA STAR WARS")
    reloj = pygame.time.Clock()


    recursos = cargar_recursos()


    nivel_datos = cargar_nivel()
    estado = "MENU"
    ejecutando = True

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        if estado == "MENU":
            reproducir_musica(recursos, RUTA_MUSICA_MENU)
            
            botones = dibujar_menu_principal(pantalla, mouse_pos, recursos["fondos"]["menu"])
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    ejecutando = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if recursos["sfx"]["click"] != None:
                        recursos["sfx"]["click"].play()
                    if botones["jugar"].collidepoint(ev.pos):
                        jugar_partida(pantalla, recursos)
                    elif botones["estadisticas"].collidepoint(ev.pos):
                        estado = "ESTADISTICAS"
                    elif botones["creditos"].collidepoint(ev.pos):
                        estado = "CREDITOS"
                    elif botones["reglas"].collidepoint(ev.pos):
                        estado = "REGLAS"
                    
                    elif botones["salir"].collidepoint(ev.pos):
                        ejecutando = False
        
        elif estado == "ESTADISTICAS":
            reproducir_musica(recursos, RUTA_MUSICA_MENU)
            lista = leer_puntajes_csv()
            rect_volver = dibujar_estadisticas(pantalla, lista, mouse_pos, recursos["fondos"]["estadisticas"])
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: ejecutando = False
                if ev.type == pygame.MOUSEBUTTONDOWN and rect_volver.collidepoint(ev.pos):
                    estado = "MENU"

        elif estado == "REGLAS":
            reproducir_musica(recursos, RUTA_MUSICA_MENU)
            rect_volver = dibujar_reglas(pantalla, mouse_pos, nivel_datos, recursos["fondos"]["reglas"])
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: ejecutando = False
                if ev.type == pygame.MOUSEBUTTONDOWN and rect_volver.collidepoint(ev.pos):
                    estado = "MENU"

        elif estado == "CREDITOS":
            reproducir_musica(recursos, RUTA_MUSICA_MENU)
            rect_volver = dibujar_creditos(pantalla, mouse_pos, recursos["fondos"]["creditos"])
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: ejecutando = False
                if ev.type == pygame.MOUSEBUTTONDOWN and rect_volver.collidepoint(ev.pos):
                    estado = "MENU"

        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()