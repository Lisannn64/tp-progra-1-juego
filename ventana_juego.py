import pygame
from renderizador import *
from config import *
from funciones import *
from archivo_csv import *

def jugar_partida(pantalla, recursos):
    
    
    reloj = pygame.time.Clock()
    
    
    fondo = recursos["fondos"]["juego"]

    imgs_dados = recursos["dados"]
    sfx = recursos["sfx"]

    nivel = cargar_nivel()
    planilla = cargar_planilla(nivel)
    dados = tirar_dados()
    bloqueados = [False]*5
    tiros = 3
    total = 0
    nombre = ""
    
    estado = "TIRAR" 

    rects_dados = []
    
    
    rects_cats = []

    reproducir_musica(recursos, RUTA_MUSICA_JUEGO, 0.4)

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
                            
                            if "anotar" in sfx:
                                sfx["anotar"].play()
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
                            
                            if recursos["sfx"]["click"] != None:
                                recursos["sfx"]["click"].play()
                    
                    
                    if rect_boton.collidepoint(ev.pos) and tiros > 0:
                        
                        if recursos["sfx"]["tirar"] != None:
                            recursos["sfx"]["tirar"].play()
                    
                        
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
                            
                            if recursos["sfx"]["anotar"] != None:
                                recursos["sfx"]["anotar"].play()
        
                            
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
            dibujar_pantalla_final(pantalla, total, nombre, recursos["fondos"]["final"])
        else:
            if fondo:
                pantalla.blit(fondo, (0,0))
            else:
                pantalla.fill(AZUL_OSCURO)

            if estado == "ELEGIR":
                modo_planilla = "ELEGIR_CATEGORIA"
            else:
                modo_planilla = ""
            rects_cats = dibujar_planilla(pantalla, planilla, total, mouse_pos, modo_planilla, dados, nivel)
        
            rect_boton = dibujar_boton_tirar(pantalla, tiros, mouse_pos)
            
            rects_dados = dibujar_dados_interactivos(pantalla, dados, bloqueados, imgs_dados, nivel)
            
            if estado == "ELEGIR":
                dibujar_texto(pantalla, "Elija la categoría!", ANCHO_VENTANA-200, 450, AMARILLO, 30)

        pygame.display.flip()
        reloj.tick(FPS)

