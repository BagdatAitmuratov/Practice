import pygame
import random
import json
import os
from random import randint

pygame.init()
WIDTH, HEIGHT = 1365, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ресурстар
bg = pygame.image.load("images/snake_bg.png")
head_img = pygame.image.load("images/head.png")
body_img = pygame.image.load("images/snake_body.png")
point_img = pygame.image.load("images/point.png")

head_original = pygame.transform.scale(head_img, (50, 50))
body_original = pygame.transform.scale(body_img, (40, 40))
point_original = pygame.transform.scale(point_img, (45, 45))

font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 100)

def save_leaderboard(username, score, level):
    data = []
    if os.path.exists("leaders.json"):
        with open("leaders.json", "r") as f:
            try: data = json.load(f)
            except: data = []
    data.append({"name": username, "score": score, "level": level})
    with open("leaders.json", "w") as f:
        json.dump(data, f, indent=4)

def get_top_leaders():
    if not os.path.exists("leaders.json"):
        return []
    with open("leaders.json", "r") as f:
        try:
            data = json.load(f)
            # Ұпай бойынша азаю ретімен сұрыптау және алғашқы 5 адамды алу
            sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
            return sorted_data[:5]
        except:
            return []

class Food:
    def __init__(self):
        self.spawn()
    def spawn(self):
        self.weight = random.choice([1, 2, 3])
        self.x = randint(100, 1200)
        self.y = randint(100, 650)
        size = 35 + self.weight * 5
        self.img = pygame.transform.scale(point_original, (size, size))
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = randint(5000, 10000)
    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.spawn()
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

class Poison:
    def __init__(self):
        self.spawn()
    def spawn(self):
        self.x = randint(100, 1200)
        self.y = randint(100, 650)
        self.radius = 20
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    def draw(self, surface):
        pygame.draw.circle(surface, (128, 0, 128), (self.x, self.y), self.radius)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def show_leaderboard_screen():
    while True:
        screen.fill((20, 20, 20))
        draw_text("TOP 5 LEADERS", big_font, (255, 215, 0), 400, 100)
        
        leaders = get_top_leaders()
        y_offset = 250
        for i, entry in enumerate(leaders):
            text = f"{i+1}. {entry['name']} - {entry['score']} pts (Lvl: {entry['level']})"
            draw_text(text, font, (255, 255, 255), 450, y_offset)
            y_offset += 60
        
        back_btn = pygame.Rect(555, 600, 250, 60)
        pygame.draw.rect(screen, (100, 100, 100), back_btn)
        draw_text("BACK", font, (255, 255, 255), 630, 610)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos): return
        
        pygame.display.flip()
        clock.tick(30)

def main_menu():
    user_name = "Bagdat"
    active = False
    while True:
        screen.fill((0, 0, 0))
        draw_text("SNAKE KBTU", big_font, (0, 255, 0), 450, 100)
        
        input_rect = pygame.Rect(530, 250, 300, 50)
        pygame.draw.rect(screen, (255, 255, 255) if active else (100, 100, 100), input_rect, 2)
        draw_text(user_name, font, (255, 255, 255), 540, 260)
        
        play_btn = pygame.Rect(555, 350, 250, 60)
        leaders_btn = pygame.Rect(555, 430, 250, 60)
        quit_btn = pygame.Rect(555, 510, 250, 60)
        
        pygame.draw.rect(screen, (50, 50, 50), play_btn)
        pygame.draw.rect(screen, (50, 50, 50), leaders_btn)
        pygame.draw.rect(screen, (50, 50, 50), quit_btn)
        
        draw_text("START", font, (255, 255, 255), 620, 360)
        draw_text("LEADERS", font, (255, 255, 255), 600, 440)
        draw_text("QUIT", font, (255, 255, 255), 635, 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos): active = True
                else: active = False
                if play_btn.collidepoint(event.pos) and user_name != "": game_loop(user_name)
                if leaders_btn.collidepoint(event.pos): show_leaderboard_screen()
                if quit_btn.collidepoint(event.pos): pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
                elif event.key == pygame.K_RETURN: active = False
                else: user_name += event.unicode
        pygame.display.flip()
        clock.tick(30)

def game_over_screen(username, score, level):
    save_leaderboard(username, score, level)
    while True:
        screen.fill((150, 0, 0))
        draw_text("GAME OVER", big_font, (0, 0, 0), 450, 200)
        draw_text(f"Score: {score}  Level: {level}", font, (255, 255, 255), 530, 350)
        btn = pygame.Rect(550, 450, 250, 60)
        pygame.draw.rect(screen, (0, 0, 0), btn)
        draw_text("MENU", font, (255, 255, 255), 625, 465)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos): return
        pygame.display.flip()

def game_loop(username):
    snake_pos = [[680, 400], [680, 440], [680, 480]]
    direction = "UP"
    change_to = "UP"
    score, level, speed = 0, 1, 10
    head_rotated = pygame.transform.rotate(head_original, -90)
    food = Food()
    poison = Poison()
    
    run = True
    while run:
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: run = False
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                    head_rotated = pygame.transform.rotate(head_original, 0)
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                    head_rotated = pygame.transform.rotate(head_original, 180)
                elif event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                    head_rotated = pygame.transform.rotate(head_original, -90)
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                    head_rotated = pygame.transform.rotate(head_original, 90)

        direction = change_to
        new_head = list(snake_pos[0])
        if direction == "UP": new_head[1] -= speed
        if direction == "DOWN": new_head[1] += speed
        if direction == "LEFT": new_head[0] -= speed
        if direction == "RIGHT": new_head[0] += speed
        
        snake_pos.insert(0, new_head)
        head_rect = pygame.Rect(new_head[0], new_head[1], 45, 45)
        
        if head_rect.colliderect(food.rect):
            score += food.weight
            if score % 5 == 0: level += 1; speed += 2
            food.spawn()
        elif head_rect.colliderect(poison.rect):
            if len(snake_pos) > 2:
                snake_pos.pop()
                snake_pos.pop()
                poison.spawn()
            else:
                run = False; game_over_screen(username, score, level)
                break
        else:
            snake_pos.pop()

        if new_head[0] < 0 or new_head[0] > 1315 or new_head[1] < 0 or new_head[1] > 718:
            run = False; game_over_screen(username, score, level)
        for block in snake_pos[1:]:
            if new_head == block:
                run = False; game_over_screen(username, score, level)

        food.update()
        food.draw(screen)
        poison.draw(screen)
        for i, pos in enumerate(snake_pos):
            img = head_rotated if i == 0 else body_original
            screen.blit(img, (pos[0], pos[1]))
        
        draw_text(f"User: {username} | Score: {score} | Lvl: {level}", font, (255, 255, 255), 20, 20)
        pygame.display.flip()
        clock.tick(30)

main_menu()