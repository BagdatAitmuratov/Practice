import pygame
import math
import datetime

pygame.init()

WIDTH, HEIGHT = 1365, 768
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
text_content = ""
typing = False
text_pos = (0, 0)

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), new_color)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    stack.append((nx, ny))

running = True
while running:
    screen.blit(base_layer, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            #курсордың кординатасы алған кез
            prevX, prevY = event.pos
            if mode == 'flood_fill':
                flood_fill(base_layer, prevX, prevY, curr_color)
            if mode == 'text':
                typing = True
                text_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            #курсор басқанға дейінгі кордината
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
            if mode == 'line':
                pygame.draw.line(base_layer, curr_color, (prevX, prevY), (currX, currY), THICKNESS)
            elif mode == 'rect':
                pygame.draw.rect(base_layer, curr_color, rect, THICKNESS)
            elif mode == 'square':
                side = max(rect.width, rect.height)
                pygame.draw.rect(base_layer, curr_color, (rect.x, rect.y, side, side), THICKNESS)
            elif mode == 'circle':
                radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
                pygame.draw.circle(base_layer, curr_color, (prevX, prevY), radius, THICKNESS)
            elif mode == 'right_triangle':
                pygame.draw.polygon(base_layer, curr_color, [(prevX, prevY), (prevX, currY), (currX, currY)], THICKNESS)
            elif mode == 'equilateral_triangle':
                height = currY - prevY
                side = 2 * height / math.sqrt(3)
                points = [(prevX, prevY), (prevX - side/2, currY), (prevX + side/2, currY)]
                pygame.draw.polygon(base_layer, curr_color, points, THICKNESS)
            elif mode == 'rhombus':
                midX, midY = (prevX + currX) / 2, (prevY + currY) / 2
                points = [(midX, prevY), (currX, midY), (midX, currY), (prevX, midY)]
                pygame.draw.polygon(base_layer, curr_color, points, THICKNESS)

        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    font = pygame.font.SysFont("Arial", THICKNESS * 5)
                    text_surface = font.render(text_content, True, curr_color)
                    base_layer.blit(text_surface, text_pos)
                    text_content = ""
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                elif event.key == pygame.K_ESCAPE:
                    text_content = ""
                    typing = False
                else:
                    text_content += event.unicode
            else:
                if event.key == pygame.K_1: THICKNESS = 2
                if event.key == pygame.K_2: THICKNESS = 5
                if event.key == pygame.K_3: THICKNESS = 10
                if event.key == pygame.K_a: mode = 'pencil'
                if event.key == pygame.K_s: mode = 'line'
                if event.key == pygame.K_d: mode = 'rect'
                if event.key == pygame.K_f: mode = 'circle'
                if event.key == pygame.K_x: mode = 'eraser'
                if event.key == pygame.K_h: mode = 'square'
                if event.key == pygame.K_j: mode = 'right_triangle'
                if event.key == pygame.K_z: mode = 'equilateral_triangle'
                if event.key == pygame.K_l: mode = 'rhombus'
                if event.key == pygame.K_q: mode = 'flood_fill'
                if event.key == pygame.K_t: mode = 'text'
                if event.key == pygame.K_r: curr_color = colorRED
                if event.key == pygame.K_g: curr_color = colorGREEN
                if event.key == pygame.K_b: curr_color = colorBLUE
                if event.key == pygame.K_k: curr_color = colorBLACK
                if event.key == pygame.K_c: base_layer.fill(colorWHITE)
                if (event.mod & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                    fn = f"save_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(base_layer, fn)

    if LMBpressed and not typing:
        rect = calculate_rect(prevX, prevY, currX, currY)
        if mode == 'line':
            pygame.draw.line(screen, curr_color, (prevX, prevY), (currX, currY), THICKNESS)
        elif mode == 'rect':
            pygame.draw.rect(screen, curr_color, rect, THICKNESS)
        elif mode == 'square':
            side = max(rect.width, rect.height)
            pygame.draw.rect(screen, curr_color, (rect.x, rect.y, side, side), THICKNESS)
        elif mode == 'circle':
            radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
            pygame.draw.circle(screen, curr_color, (prevX, prevY), radius, THICKNESS)
        elif mode == 'right_triangle':
            pygame.draw.polygon(screen, curr_color, [(prevX,prevY),(prevX,currY),(currX,currY)], THICKNESS)
        elif mode == 'equilateral_triangle':
            height = currY - prevY
            side = 2 * height / math.sqrt(3)
            points = [(prevX, prevY), (prevX - side/2, currY), (prevX + side/2, currY)]
            pygame.draw.polygon(screen, curr_color, points, THICKNESS)
        elif mode == 'rhombus':
            midX, midY = (prevX + currX) / 2, (prevY + currY) / 2
            points = [(midX, prevY), (currX, midY), (midX, currY), (prevX, midY)]
            pygame.draw.polygon(screen, curr_color, points, THICKNESS)

    if typing:
        font = pygame.font.SysFont("Arial", THICKNESS * 5)
        img = font.render(text_content + "|", True, curr_color)
        screen.blit(img, text_pos)

    font_hud = pygame.font.SysFont("Arial", 18)
    instructions = [
        f"MODE: {mode.upper()}",
        f"SIZE: {THICKNESS}",
        "A-Pencil, S-Line, D-Rect, F-Circle",
        "H-Square, J-RightTri, Z-EquiTri, L-Rhombus",
        "Q-Fill, T-Text, X-Eraser",
        "1, 2, 3 - Brush Size",
        "R, G, B, K - Colors, C - Clear",
        "Ctrl + S - Save"
    ]
    for i, text in enumerate(instructions):
        txt = font_hud.render(text, True, (0, 0, 0))
        pygame.draw.rect(screen, (200, 200, 200), (10, 10 + i*22, txt.get_width() + 10, 20))
        screen.blit(txt, (15, 10 + i*22))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()