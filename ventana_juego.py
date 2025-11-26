import pygame
from config import *

pygame.init()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption(TITULO_JUEGO)
reloj = pygame.time.Clock()


ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    pantalla.fill((ROJO))
    pygame.display.flip()

    reloj.tick(30) #acá van los fps

pygame.quit()