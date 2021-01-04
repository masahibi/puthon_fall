import pygame

screen = pygame.display.set_mode((800, 600))
RED = (255, 0, 0)
while True:
    pygame.draw.rect(screen, RED, (100, 50, 150, 200))
    pygame.display.flip()