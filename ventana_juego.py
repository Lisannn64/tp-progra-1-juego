import pygame

pygame.init()

pantalla = pygame.display.set_mode((600,300))
pygame.display.set_caption("Texto de prueba")
reloj = pygame.time.Clock()

ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    pantalla.fill((255, 0, 0))
    pygame.display.flip()

    reloj.tick(30) #acá van los fps

pygame.quit()