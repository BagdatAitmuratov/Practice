import pygame
import time
from random import randint
import random

pygame.init()
screen = pygame.display.set_mode((1365,768))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# суреттер
bg = pygame.image.load("images/snake_bg.png")
head_img = pygame.image.load("images/head.png")
body_img = pygame.image.load("images/snake_body.png")
point_img = pygame.image.load("images/point.png")

head_original = pygame.transform.scale(head_img, (50, 50))
body_original = pygame.transform.scale(body_img, (40, 40))
point_original = pygame.transform.scale(point_img, (45, 45))

# Бастапқы басы (бұрылу үшін айнымалы)
head_rotated = head_original

font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 100)

class Food:
    def __init__(self):
        self.spawn()
        
    def spawn(self):
        self.weight = random.choice([1, 2, 3])
        size = 30 + (self.weight * 4)
        self.img = pygame.transform.scale(point_original, (size, size))
        self.x = randint(100, 1200)
        self.y = randint(100, 650)
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = randint(4000, 8000)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.spawn()

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

# Ойынды басына қайтару функциясы
def reset_game():
    # Басында тек бір ғана басы болады, бағыт тоқтап тұрады
    return [[682, 400]], "STOP", 0, False, 10

# Параметрлерді жүктеу
snake_pos, direction, score, game_over, speed = reset_game()
change_to = direction
food = Food()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Бағытты өзгерту және басты бұру логикасы
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                    head_rotated = pygame.transform.rotate(head_original, -90)
                if event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                    head_rotated = pygame.transform.rotate(head_original, 90)
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                    head_rotated = pygame.transform.rotate(head_original, 0)
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                    head_rotated = pygame.transform.rotate(head_original, 180)
            else:
                if event.key == pygame.K_SPACE: 
                    snake_pos, direction, score, game_over, speed = reset_game()
                    change_to = "STOP"
                    head_rotated = head_original
                    food.spawn()

    if not game_over:
        direction = change_to
        
        # Қозғалыс тек STOP болмағанда басталады
        if direction != "STOP":
            new_head = list(snake_pos[0])
            
            if direction == "UP":    new_head[1] -= speed
            if direction == "DOWN":  new_head[1] += speed
            if direction == "LEFT":  new_head[0] -= speed
            if direction == "RIGHT": new_head[0] += speed
            
            snake_pos.insert(0, new_head)
            
            # Тамақ жеуді тексеру
            head_rect = pygame.Rect(new_head[0], new_head[1], 45, 45)
            if head_rect.colliderect(food.rect):
                score += food.weight
                # Жылдамдықты арттыру (әр 10 ұпай сайын)
                if score % 10 == 0:
                    speed += 1
                food.spawn()
                # Алма жегенде pop() жасамаймыз, жылан ұзарады
            else:
                snake_pos.pop()

            # Қабырғаға соғылу
            if new_head[0] < 0 or new_head[0] > 1315 or new_head[1] < 0 or new_head[1] > 718:
                game_over = True
                
            # Өзіне соғылу (тек жылан ұзарғанда мүмкін)
            for block in snake_pos[1:]:
                if new_head == block:
                    game_over = True

        # СУРЕТ САЛУ
        screen.blit(bg, (0, 0))
        food.update()
        food.draw(screen)
        
        for i, pos in enumerate(snake_pos):
            if i == 0:
                screen.blit(head_rotated, (pos[0], pos[1]))
            else:
                screen.blit(body_original, (pos[0], pos[1])) 
        
        score_text = font.render(f"Score: {score}  Speed: {speed}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    else:
        # Game Over экраны
        screen.fill((255, 0, 0))
        over_text = big_font.render("GAME OVER", True, (0, 0, 0))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        retry_text = font.render("Press SPACE to Restart", True, (0, 0, 0))
        
        screen.blit(over_text, (450, 250))
        screen.blit(final_score, (550, 350))
        screen.blit(retry_text, (500, 450))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()