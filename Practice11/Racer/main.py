import pygame
import random
import time
import sys

# Ойынды инициализациялау
pygame.init()
WIDTH, HEIGHT = 840, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer: Mud & Intro Edition")
clock = pygame.time.Clock()

# Ресурстарды жүктеу (Жолдарын тексеріп алыңыз)
try:
    bg = pygame.image.load("image/racer_bg.png")
    player_img = pygame.image.load("image/up_player.png")
    car_img = pygame.image.load("image/up_car.png")
    coin_img = pygame.image.load("image/up_coin.png")
    # Балшық үшін кішкене қоңыр тіктөртбұрыш немесе сурет
    mud_img = pygame.Surface((100, 60))
    mud_img.fill((101, 67, 33)) # Қоңыр түс
    
    avaria_sound = pygame.mixer.Sound("sound/avaria.mp3")
except:
    print("Ресурстар табылмады! Сурет жолдарын тексеріңіз.")

# Қаріптер
font_big = pygame.font.SysFont("Comic Sans MS", 60, True)
font_small = pygame.font.SysFont("Comic Sans MS", 30, True)

# Глобалдық айнымалылар
speed_car = 4
score = 0
sum_coin = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(420, 580))
        self.base_speed = 8
        self.speed = 8
        self.slow_timer = 0

    def update(self):
        # Балшық эффектісін тексеру
        if time.time() < self.slow_timer:
            self.speed = 3  # Баяу жылдамдық
        else:
            self.speed = self.base_speed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 125:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 650:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_img
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -100))

    def update(self):
        global score, speed_car
        self.rect.y += speed_car
        if self.rect.top > HEIGHT:
            score += 1
            if score % 5 == 0: # Әр 5 машина сайын жылдамдық артады
                speed_car += 1
            self.rect.y = -100
            self.rect.x = random.randint(150, 650)

class Mud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mud_img
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -500))

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-1500, -1000)
            self.rect.x = random.randint(150, 650)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -100))

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.y = -100
            self.rect.x = random.randint(150, 650)

def show_intro():
    intro = True
    while intro:
        screen.fill((50, 50, 50))
        title = font_big.render("RACER GAME", True, (255, 215, 0))
        instr = font_small.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 350))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
        pygame.display.update()

def game_loop():
    global score, sum_coin, speed_car
    score = 0
    sum_coin = 0
    speed_car = 4
    
    P1 = Player()
    E1 = Enemy()
    C1 = Coin()
    M1 = Mud()
    
    enemies = pygame.sprite.Group(E1)
    coins = pygame.sprite.Group(C1)
    muds = pygame.sprite.Group(M1)
    all_sprites = pygame.sprite.Group(P1, E1, C1, M1)
    
    bg_y = 0
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Фонды жылжыту
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - HEIGHT))
        bg_y = (bg_y + 5) % HEIGHT

        # Жаңарту
        all_sprites.update()

        # Коллизиялар (Соқтығысулар)
        if pygame.sprite.spritecollideany(P1, enemies):
            avaria_sound.play()
            return score, sum_coin # Ойын бітті

        if pygame.sprite.spritecollide(P1, coins, True):
            sum_coin += random.randint(1, 3)
            new_c = Coin()
            coins.add(new_c); all_sprites.add(new_c)

        if pygame.sprite.spritecollideany(P1, muds):
            P1.slow_timer = time.time() + 2 # 2 секундқа баяулау

        # Сурет салу
        all_sprites.draw(screen)
        
        s_txt = font_small.render(f"Score: {score}", True, (0,0,0))
        c_txt = font_small.render(f"Coins: {sum_coin}", True, (0,0,0))
        screen.blit(s_txt, (10, 10))
        screen.blit(c_txt, (10, 45))

        pygame.display.flip()
        clock.tick(60)

def game_over_screen(s, c):
    while True:
        screen.fill((255, 0, 0))
        go_txt = font_big.render("GAME OVER", True, (0,0,0))
        res_txt = font_small.render(f"Final Score: {s} | Coins: {c}", True, (0,0,0))
        hint_txt = font_small.render("SPACE to Restart | M for Menu", True, (255, 255, 255))
        
        screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, 200))
        screen.blit(res_txt, (WIDTH//2 - res_txt.get_width()//2, 300))
        screen.blit(hint_txt, (WIDTH//2 - hint_txt.get_width()//2, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: return True
                if event.key == pygame.K_m: return False
        pygame.display.update()

# Негізгі программа ағыны
while True:
    show_intro()
    final_s, final_c = game_loop()
    if not game_over_screen(final_s, final_c):
        continue # Мәзірге қайту