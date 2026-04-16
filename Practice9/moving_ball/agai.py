# Boundary checking - keeping the circle inside the screen

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RADIUS = 40
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
movement_speed = 5

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        circle_y -= movement_speed
    if keys[pygame.K_DOWN]:
        circle_y += movement_speed
    if keys[pygame.K_RIGHT]:
        circle_x += movement_speed
    if keys[pygame.K_LEFT]:
        circle_x -= movement_speed

    # Clamp to screen boundaries (accounting for radius)
    if circle_x - RADIUS < 0:
        circle_x = RADIUS
    if circle_x + RADIUS > WIDTH:
        circle_x = WIDTH - RADIUS
    if circle_y - RADIUS < 0:
        circle_y = RADIUS
    if circle_y + RADIUS > HEIGHT:
        circle_y = HEIGHT - RADIUS

    screen.fill("white")
    pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()