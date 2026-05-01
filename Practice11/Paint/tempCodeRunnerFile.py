import pygame
import math

pygame.init()

WIDTH = 1365
HEIGHT = 768
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

prevX, prevY = 0, 0
currX, currY = 0, 0

#4бұрыш фунуция
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
            rect = calculate_rect(prevX, prevY, currX, currY)
            
            if mode == 'rect':
                pygame.draw.rect(base_layer, curr_color, rect, THICKNESS)
            elif mode == 'square':
                side = max(rect.width, rect.height)
                pygame.draw.rect(base_layer, curr_color, (rect.x, rect.y, side, side), THICKNESS)
            elif mode == 'circle':
                radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
                pygame.draw.circle(base_layer, curr_color, (prevX, prevY), radius, THICKNESS)
            elif mode == 'right_triangle':
                points = [(prevX, prevY), (prevX, currY), (currX, currY)]
                pygame.draw.polygon(base_layer, curr_color, points, THICKNESS)
            elif mode == 'equilateral_triangle':
                height = currY - prevY
                side = 2 * height / math.sqrt(3)
                points = [(prevX, prevY), (prevX - side/2, currY), (prevX + side/2, currY)]
                pygame.draw.polygon(base_layer, curr_color, points, THICKNESS)
            elif mode == 'rhombus':
                midX = (prevX + currX) / 2
                midY = (prevY + currY) / 2
                points = [(midX, prevY), (currX, midY), (midX, currY), (prevX, midY)]
                pygame.draw.polygon(base_layer, curr_color, points, THICKNESS)

        if event.type == pygame.KEYDOWN:
            #іс әрекет таңдау
            if event.key == pygame.K_1: mode = 'pencil'
            if event.key == pygame.K_2: mode = 'rect'
            if event.key == pygame.K_3: mode = 'circle'
            if event.key == pygame.K_4: mode = 'eraser'
            if event.key == pygame.K_5: mode = 'square'
            if event.key == pygame.K_6: mode = 'right_triangle'
            if event.key == pygame.K_7: mode = 'equilateral_triangle'
            if event.key == pygame.K_8: mode = 'rhombus'

            #түстер
            if event.key == pygame.K_r: curr_color = colorRED
            if event.key == pygame.K_g: curr_color = colorGREEN
            if event.key == pygame.K_b: curr_color = colorBLUE
            if event.key == pygame.K_k: curr_color = colorBLACK
            if event.key == pygame.K_c: base_layer.fill(colorWHITE)

    if LMBpressed:
        rect = calculate_rect(prevX, prevY, currX, currY)
        if mode == 'rect':
            pygame.draw.rect(screen, curr_color, rect, THICKNESS)
        elif mode == 'square':
            side = max(rect.width, rect.height)
            pygame.draw.rect(screen, curr_color, (rect.x, rect.y, side, side), THICKNESS)
        elif mode == 'circle':
            radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
            pygame.draw.circle(screen, curr_color, (prevX, prevY), radius, THICKNESS)
        elif mode == 'right_triangle':
            pygame.draw.polygon(screen, curr_color, [(prevX, prevY), (prevX, currY), (currX, currY)], THICKNESS)
        elif mode == 'equilateral_triangle':
            height = currY - prevY
            side = 2 * height / math.sqrt(3)
            points = [(prevX, prevY), (prevX - side/2, currY), (prevX + side/2, currY)]
            pygame.draw.polygon(screen, curr_color, points, THICKNESS)
        elif mode == 'rhombus':
            midX, midY = (prevX + currX) / 2, (prevY + currY) / 2
            points = [(midX, prevY), (currX, midY), (midX, currY), (prevX, midY)]
            pygame.draw.polygon(screen, curr_color, points, THICKNESS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()