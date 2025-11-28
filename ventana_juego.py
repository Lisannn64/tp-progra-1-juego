import pygame
from renderizador import *
from config import *
from funciones import *
from archivo_csv import *

def jugar_partida(pantalla):
    
    reloj = pygame.time.Clock()
    
    nivel = cargar_nivel()
    planilla = cargar_planilla(nivel)
    dados = tirar_dados()
    bloqueados = [False]*5
    tiros = 3
    total = 0
    nombre = ""
    
    estado = "TIRAR" 
    
    rects_dados = []
    rect_boton = pygame.Rect(0,0,0,0)
    rects_cats = []


    jugando = True
    while jugando:
        mouse_pos = pygame.mouse.get_pos()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if estado == "NOMBRE":
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        if nombre.strip():
                            guardar_puntaje(nombre, total)
                            jugando = False 
                    elif ev.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        if len(nombre) < 12: nombre += ev.unicode
            
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if estado == "TIRAR":
                    for i, r in enumerate(rects_dados):
                        if r.collidepoint(ev.pos):
                            bloqueados[i] = not bloqueados[i]
                    
                    if rect_boton.collidepoint(ev.pos) and tiros > 0:
                        nuevos = []
                        for i in range(5):
                            if bloqueados[i]: nuevos.append(dados[i])
                            else: nuevos.append(random.randint(1,6))
                        dados = nuevos
                        tiros -= 1
                        if tiros == 0: estado = "ELEGIR"
                
                elif estado == "ELEGIR":
                    for cat, r in rects_cats:
                        if r.collidepoint(ev.pos):
                            pts = calcular_puntaje(cat, dados, nivel)
                            planilla[cat] = pts
                            
                            suma = 0
                            lleno = True
                            for v in planilla.values():
                                if v is None: lleno = False
                                else: suma += v
                            total = suma
                            
                            if lleno:
                                estado = "NOMBRE"
                            else:
                                dados = tirar_dados()
                                bloqueados = [False]*5
                                tiros = 3
                                estado = "TIRAR"
                            break

        if estado == "NOMBRE":
            dibujar_pantalla_final(pantalla, total, nombre)
        else:
            pantalla.fill(ROJO)
            dibujar_planilla(pantalla, planilla, total, mouse_pos, "ELEGIR_CATEGORIA" if estado == "ELEGIR" else "", dados, nivel)
            rects_cats = obtener_rects_planilla(planilla)
            rect_boton = dibujar_boton_tirar(pantalla, tiros)
            rects_dados = dibujar_dados_interactivos(pantalla, dados, bloqueados)
            
            if estado == "ELEGIR":
                dibujar_texto(pantalla, "Elija la categoría!", ANCHO_VENTANA-150, 200, AMARILLO, 30)

        pygame.display.flip()
        reloj.tick(FPS)

