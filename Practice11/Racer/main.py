import pygame
from random import randint
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((840,650))
pygame.display.set_caption("Racer")
bg = pygame.image.load("image/racer_bg.png")

bg_y = 0
bg_hight=bg.get_height()

run = True
while run:
    screen.blit(bg,(0,0))
    screen.blit(bg,(0,bg_y))
    screen.blit(bg,(0,bg_y-650))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

    bg_y += 5
    if bg_y >= bg_hight:
        bg_y =0
    
    clock.tick(60)
pygame.quit()
    
