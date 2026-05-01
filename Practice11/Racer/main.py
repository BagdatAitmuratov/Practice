import pygame
import random
from random import randint
import time
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((840,650))
pygame.display.set_caption("Racer")


bg = pygame.image.load("image/racer_bg.png")
player = pygame.image.load("image/up_player.png")
car = pygame.image.load("image/up_car.png")
coin = pygame.image.load("image/up_coin.png")
avaria_sound = pygame.mixer.Sound("sound/avaria.mp3")
music = pygame.mixer.Sound("sound/music1.wav")

font = pygame.font.SysFont("Comic Sans MS",60,True)
scores_font = pygame.font.SysFont("Comic Sans MS",30,True)

bg_y = 0
bg_hight=bg.get_height()


score =0
sum_coin =0
speed_car=4

#кластар--------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = (420,580)
        self.speed = 8
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 125:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 650:
            self.rect.x += self.speed
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        
        self.image = car
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(125,675)
        self.rect.y = -100

    def update(self):
        global score,speed_car
        self.rect.y += speed_car
        if self.rect.top > 650:
            score += 1
        
            if sum_coin % 5 == 0:
                speed_car += 2
            self.rect.y = -100
            self.rect.x = random.randint(125,675)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =coin
        self.rect = self.image.get_rect()
        if score%3==0 or score%4==0:
                self.rect.center = (randint(175,675),-100)
    def speed_coin(self):
        self.rect.move_ip(0,5)
        if self.rect.top>650:
            self.rect.top = 0
#class------------------------------------------------------\
#класстардың қосылуы
P1 = Player()
E1 = Enemy()
C0in  = Coin()
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C0in)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C0in)




run = True
while run:
    screen.blit(bg,(0,0))
    screen.blit(bg,(0,bg_y))
    screen.blit(bg,(0,bg_y-650))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #шекара-----------------------
    #75----675
    #----------------------------
    P1.update()
    E1.update()
    C0in.speed_coin()
    if pygame.sprite.spritecollideany(P1,enemies):
        avaria_sound.play()
        run=False
    if pygame.sprite.spritecollideany(P1,coins):
        #random coin sums---------
        sum_coin += randint(1,3)
        C0in.rect.top = -100
        C0in.rect.center = (randint(175,675),-100)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        avaria_sound.play()
        time.sleep(0.5)
        
        screen.fill((255,0,0))
        game_over = font.render("GAME OVER", True, (0,0,0))
        res_score = font.render(f"Score: {score}", True, (0,0,0))
        coins_score = font.render(f"Coins:{sum_coin}", True,(0,0,0))
        screen.blit(game_over, (240, 225))
        screen.blit(res_score, (240, 325))
        screen.blit(coins_score,(240, 425))
        pygame.display.flip()
        
        time.sleep(5)
        running = False



    scores= scores_font.render(f"Score: {score}",True,(0,0,0))
    coin_s = scores_font.render(f"Coin: {sum_coin}",True,(0,0,0))
    screen.blit(scores,(10,10))
    screen.blit(coin_s,(10,40))



    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    #фон жүрісі
    bg_y += 5
    if bg_y >= bg_hight:
        bg_y =0
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
    
