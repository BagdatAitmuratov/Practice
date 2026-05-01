import pygame
import random
from random import randint

# --- 1. БАСТАПҚЫ ОРНАТУ ---
pygame.init()
WIDTH, HEIGHT = 1365, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Суреттерді жүктеу
bg = pygame.image.load("images/snake_bg.png")
head_img = pygame.image.load("images/head.png")
body_img = pygame.image.load("images/snake_body.png")
point_img = pygame.image.load("images/point.png")

# Түпнұсқа суреттер (бұру үшін керек)
head_original = pygame.transform.scale(head_img, (50, 50))
body_draw = pygame.transform.scale(body_img, (40, 40))
point_base = pygame.transform.scale(point_img, (45, 45))

# Бастапқы басы (оңға қарап тұрған күйі)
head_rotated = head_original

font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 100)

# --- 2. ТАҒАМ КЛАСЫ ---
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.weight = random.choice([1, 3, 5])
        size = 30 + (self.weight * 6)
        self.img = pygame.transform.scale(point_base, (size, size))
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 100)
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = randint(4000, 8000)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.spawn()

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

# --- 3. ФУНКЦИЯЛАР ---
def reset_game():
    return [[682, 400], [667, 400], [652, 400]], "RIGHT", 0, False, 7

# Бастапқы параметрлер
snake_pos, direction, score, game_over, speed = reset_game()
change_to = direction
food = Food()
run = True

# --- 4. НЕГІЗГІ ЦИКЛ ---
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Сіздің кодыңыздағы басты бұру логикасын осында қостық
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
            else:
                if event.key == pygame.K_SPACE:
                    snake_pos, direction, score, game_over, speed = reset_game()
                    change_to = direction
                    head_rotated = head_original # Қайта басталғанда басын қалпына келтіру
                    food.spawn()

    if not game_over:
        direction = change_to
        new_head = list(snake_pos[0])

        # Қозғалыс
        if direction == "UP":    new_head[1] -= speed
        if direction == "DOWN":  new_head[1] += speed
        if direction == "LEFT":  new_head[0] -= speed
        if direction == "RIGHT": new_head[0] += speed

        snake_pos.insert(0, new_head)
        head_rect = pygame.Rect(new_head[0], new_head[1], 45, 45)

        # Тамақ жеу және Жылдамдықты арттыру
        if head_rect.colliderect(food.rect):
            score += 1
            # Әр 3 тамақ жеген сайын жылдамдықты 2-ге арттыру (сіздің кодыңыздағыдай)
            if score % 3 == 0:
                speed += 2
            
            food.spawn()
            # Ұзару үшін pop() жасамаймыз
        else:
            snake_pos.pop()

        # Шетіне немесе денесіне соғылу
        if new_head[0] < 0 or new_head[0] > WIDTH - 50 or new_head[1] < 0 or new_head[1] > HEIGHT - 50:
            game_over = True
        for block in snake_pos[1:]:
            if new_head == block:
                game_over = True

        # СУРЕТ САЛУ
        screen.blit(bg, (0, 0))
        food.update()
        food.draw(screen)

        for i, pos in enumerate(snake_pos):
            if i == 0:
                screen.blit(head_rotated, (pos[0], pos[1])) # Бұрылған бас
            else:
                screen.blit(body_draw, (pos[0], pos[1])) # Дене

        text = font.render(f"Score: {score}  Speed: {speed}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

    else:
        # Game Over Экраны
        screen.fill((255, 0, 0))
        over_text = big_font.render("GAME OVER", True, (0, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        retry_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
        
        screen.blit(over_text, (WIDTH//2 - 250, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(retry_text, (WIDTH//2 - 200, HEIGHT//2 + 80))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()