import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255)) 

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorGREEN = (0, 255, 0)
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5
curr_color = colorBLACK
mode = 'pencil' 

prevX = 0
prevY = 0
currX = 0
currY = 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True
while running:
    screen.blit(base_layer, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos

        if event.type == pygame.MOUSEMOTION:
            currX, currY = event.pos
            if LMBpressed:
                if mode == 'pencil':
                    pygame.draw.line(base_layer, curr_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                elif mode == 'eraser':
                    pygame.draw.line(base_layer, colorWHITE, (prevX, prevY), (currX, currY), THICKNESS * 4)
                    prevX, prevY = currX, currY

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            if mode == 'rect':
                pygame.draw.rect(base_layer, curr_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif mode == 'circle':
                radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
                pygame.draw.circle(base_layer, curr_color, (prevX, prevY), radius, THICKNESS)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1: mode = 'pencil'
            if event.key == pygame.K_2: mode = 'rect'
            if event.key == pygame.K_3: mode = 'circle'
            if event.key == pygame.K_4: mode = 'eraser'
            

            if event.key == pygame.K_r: curr_color = colorRED
            if event.key == pygame.K_g: curr_color = colorGREEN
            if event.key == pygame.K_b: curr_color = colorBLUE
            if event.key == pygame.K_k: curr_color = colorBLACK
            if event.key == pygame.K_c: base_layer.fill(colorWHITE)


    if LMBpressed:
        if mode == 'rect':
            pygame.draw.rect(screen, curr_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
        elif mode == 'circle':
            radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
            pygame.draw.circle(screen, curr_color, (prevX, prevY), radius, THICKNESS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()