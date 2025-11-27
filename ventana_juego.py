import pygame
from renderizador import *
from config import *
from funciones import *

def main_grafico():
    
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(TITULO_JUEGO)
    reloj = pygame.time.Clock()


    nivel = cargar_nivel()
    PANTALLA_ACTUAL = cargar_planilla(nivel)

    DADOS_VALORES = tirar_dados()
    DADOS_BLOQUEADOS = [False] * 5
    TIRADAS_RESTANTES = 3
    PUNTAJE_TOTAL = 0
    PLANILLA_ACTUAL = cargar_planilla(cargar_nivel())
    ESTADO_JUEGO = "ESPERANDO_TIRADA"

    RECTS_DADOS = []
    RECT_BOTON_TIRAR = pygame.Rect(0, 0, 0, 0)
    RECTS_CATEGORIAS = []


    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
    
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_clic = evento.pos
        
                if RECT_BOTON_TIRAR.collidepoint(pos_clic):
                    if ESTADO_JUEGO == "ESPERANDO_TIRADA" and TIRADAS_RESTANTES > 0:
                        DADOS_VALORES, TIRADAS_RESTANTES, DADOS_BLOQUEADOS = manejar_tirada(
                        DADOS_VALORES, DADOS_BLOQUEADOS, TIRADAS_RESTANTES
                        )
                
                        if TIRADAS_RESTANTES == 0:
                            ESTADO_JUEGO = "ELEGIR_CATEGORIA"
                            print(f"Turno final! Ahora debes hacer clic en una categoría de la planilla ")

                elif ESTADO_JUEGO == "ESPERANDO_TIRADA":
                    DADOS_BLOQUEADOS = gestionar_clic(DADOS_BLOQUEADOS, RECTS_DADOS, pos_clic)

                elif ESTADO_JUEGO == "ELEGIR_CATEGORIA":
                    for categoria, rect_cat in RECTS_CATEGORIAS:
                        if rect_cat.collidepoint(pos_clic):

                            nivel_datos = cargar_nivel()
                            puntos = calcular_puntaje(categoria, DADOS_VALORES, nivel_datos)

                            PLANILLA_ACTUAL[categoria] = puntos
                            print(f"ANOTADO: {categoria} por {puntos} puntos.")

                            nuevo_total = 0
                            for p in PLANILLA_ACTUAL.values():
                                if p == None:
                                    pass
                                else:
                                    nuevo_total += p
                                
                            PUNTAJE_TOTAL = nuevo_total

                            DADOS_VALORES = tirar_dados()
                            DADOS_BLOQUEADOS = [False] * 5
                            TIRADAS_RESTANTES = 3
                            ESTADO_JUEGO = "ESPERANDO_TIRADA"
                            break

    
        pantalla.fill(ROJO)
        RECTS_CATEGORIAS = obtener_rects_planilla(PLANILLA_ACTUAL)
        dibujar_planilla(pantalla, PANTALLA_ACTUAL, PUNTAJE_TOTAL)
        RECT_BOTON_TIRAR = dibujar_boton_tirar(pantalla, TIRADAS_RESTANTES)
        RECTS_DADOS = dibujar_dados_interactivos(pantalla, DADOS_VALORES, DADOS_BLOQUEADOS)

        if ESTADO_JUEGO == "ELEGIR_CATEGORIA":
            dibujar_texto(pantalla, "Elegí la categoría!", ANCHO_VENTANA - 150, 200, AMARILLO, 30)
        
        pygame.display.flip()
        reloj.tick(FPS) #acá van los fps

    pygame.quit()


if __name__ == "__main__":
    main_grafico()