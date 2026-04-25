import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 840, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


bg = pygame.image.load("image/racer_bg.png")
player_img = pygame.image.load("image/up_player.png") 
enemy_img = pygame.image.load("image/up_car.png")

pygame.mixer.music.load("sound/music_taxi.mp3")
pygame.mixer.music.play(-1) 
crash_sound = pygame.mixer.Sound("sound/avaria.mp3")


font = pygame.font.SysFont("Verdana", 60)
score_font = pygame.font.SysFont("Verdana", 20)

clock = pygame.time.Clock()

SCORE = 0
ENEMY_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, WIDTH - 100)
        self.rect.y = -100

    def update(self):
        global SCORE, ENEMY_SPEED
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            SCORE += 1
        
            if SCORE % 3 == 0:
                ENEMY_SPEED += 1
            self.rect.y = -100
            self.rect.x = random.randint(100, WIDTH - 100)

P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()


    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()
        time.sleep(0.5)
        
        screen.fill(RED)
        game_over = font.render("GAME OVER", True, BLACK)
        res_score = font.render(f"Score: {SCORE}", True, BLACK)
        screen.blit(game_over, (WIDTH//2 - 180, HEIGHT//2 - 100))
        screen.blit(res_score, (WIDTH//2 - 120, HEIGHT//2))
        pygame.display.flip()
        
        time.sleep(2)
        running = False
    screen.blit(bg, (0, 0))
    scores = score_font.render(f"Score: {SCORE}", True, BLACK)
    screen.blit(scores, (10, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()