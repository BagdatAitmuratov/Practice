import pygame

def draw_text(screen, text, size, x, y, color=(0, 0, 0)):
    font = pygame.font.SysFont("Comic Sans MS", size, True)
    surf = font.render(str(text), True, color)
    screen.blit(surf, (x, y))

class Button:
    def __init__(self, text, x, y, w, h, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 25, True)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        txt = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def get_user_name(screen):
    name = ""
    font = pygame.font.SysFont("Arial", 40, True)
    input_active = True
    while input_active:
        screen.fill((255, 255, 255))
        draw_text(screen, "Enter Your Name:", 40, 250, 200)
        
        name_surf = font.render(name, True, (0, 0, 255))
        screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 300))
        draw_text(screen, "Press ENTER to Save", 20, 320, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "Guest"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10: name += event.unicode
        pygame.display.flip()
    return name