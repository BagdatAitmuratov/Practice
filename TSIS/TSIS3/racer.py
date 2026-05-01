import pygame
import random

WIDTH, HEIGHT = 840, 650

class Player(pygame.sprite.Sprite):
    def __init__(self, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-70))
        self.speed = 8
        self.shield = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 125:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 650:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img_path, speed):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect(center=(random.randint(125, 650), -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, img_path, weight):
        super().__init__()
        self.weight = weight
        base_img = pygame.image.load(img_path)
        size = 20 + (weight * 10)
        self.image = pygame.transform.scale(base_img, (size, size))
        self.rect = self.image.get_rect(center=(random.randint(150, 600), -50))

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        colors = {'nitro': (255, 255, 0), 'shield': (0, 0, 255), 'repair': (255, 0, 255)}
        self.image.fill(colors[type])
        self.rect = self.image.get_rect(center=(random.randint(150, 600), -50))

    def update(self):
        self.rect.y += 4
        if self.rect.top > HEIGHT:
            self.kill()