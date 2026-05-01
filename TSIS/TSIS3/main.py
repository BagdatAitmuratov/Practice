import pygame
import random
import time
import json
import sys

pygame.init()
WIDTH, HEIGHT = 840, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Racer")
clock = pygame.time.Clock()

try:
    bg = pygame.image.load("assets/image/racer_bg.png")
    player_img = pygame.image.load("assets/image/up_player.png")
    car_img = pygame.image.load("assets/image/up_car.png")
    coin_img = pygame.image.load("assets/image/up_coin.png")
    kedergi_img = pygame.image.load("assets/image/up_kedergi.png")
    avaria_sound = pygame.mixer.Sound("assets/sounds/avaria.mp3")
    pygame.mixer.music.load("assets/sounds/music1.wav")
except:
    print("Ресурстар табылмады!")

font_menu = pygame.font.SysFont("Comic Sans MS", 50, True)
font_small = pygame.font.SysFont("Comic Sans MS", 30, True)
font_tiny = pygame.font.SysFont("Comic Sans MS", 20, True)

def load_json(file, default):
    try:
        with open(file, 'r') as f: return json.load(f)
    except: return default

def save_json(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=2)

settings = load_json('settings.json', {"sound": True})
leaderboard = load_json('leaderboard.json', [])

if settings["sound"]:
    pygame.mixer.music.play(-1)

def get_user_name():
    name = ""
    input_active = True
    while input_active:
        screen.fill((50, 50, 50))
        txt = font_menu.render("Enter Your Name:", True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 200))
        name_txt = font_menu.render(name + "|", True, (255, 215, 0))
        screen.blit(name_txt, (WIDTH//2 - name_txt.get_width()//2, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "": input_active = False
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                else:
                    if len(name) < 12: name += event.unicode
        pygame.display.flip()
    return name.strip()

class Button:
    def __init__(self, text, x, y, w, h, color=(100, 100, 100)):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        txt = font_small.render(self.text, True, (255, 255, 255))
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(420, 580))
        self.speed = 8
        self.has_shield = False
    def update(self, diff=0):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 125: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 650: self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, is_car=True):
        super().__init__()
        self.image = car_img if is_car else kedergi_img
        self.is_car = is_car
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -100))
        self.base_speed = random.randint(3, 6) if is_car else 0
    def update(self, diff):
        bg_speed = 5 + diff 
        self.rect.y += (bg_speed + self.base_speed)
        if self.rect.top > HEIGHT:
            if self.is_car:
                global score
                score += 1
            self.rect.center = (random.randint(150, 650), -100)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 2, 3])
        size = int(40 * (0.5 + self.value * 0.25))
        self.image = pygame.transform.scale(coin_img, (size, size))
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -100))
    def update(self, diff):
        self.rect.y += (5 + diff)
        if self.rect.top > HEIGHT: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((40, 40))
        if self.type == "nitro": self.color = (0, 0, 255)
        elif self.type == "shield": self.color = (0, 255, 0)
        else: self.color = (255, 0, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(random.randint(150, 650), -50))
    def update(self, diff):
        self.rect.y += (5 + diff)
        if self.rect.top > HEIGHT: self.kill()

def game_loop():
    global score
    score = 0
    sum_coins, distance = 0, 0.0
    nitro_timer = 0
    p = Player()
    enemies = pygame.sprite.Group(Enemy(True), Enemy(False))
    coins_group = pygame.sprite.Group()
    powerups_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(p)
    for e in enemies: all_sprites.add(e)
    bg_y = 0
    while True:
        current_diff = score // 5
        bonus_speed = 7 if nitro_timer > time.time() else 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        enemy_hit = pygame.sprite.spritecollideany(p, enemies)
        if enemy_hit:
            if p.has_shield:
                p.has_shield = False
                enemy_hit.rect.y = -200
            else:
                avaria_sound.play()
                return score, sum_coins, int(distance)
        hit_coins = pygame.sprite.spritecollide(p, coins_group, True)
        for c in hit_coins: sum_coins += c.value
        hit_pw = pygame.sprite.spritecollide(p, powerups_group, True)
        for pw in hit_pw:
            if pw.type == "nitro": nitro_timer = time.time() + 5
            elif pw.type == "shield": p.has_shield = True
            elif pw.type == "repair":
                for e in enemies: e.rect.y = -200
        if random.randint(1, 100) == 1:
            new_coin = Coin(); coins_group.add(new_coin); all_sprites.add(new_coin)
        if random.randint(1, 250) == 1:
            new_pw = PowerUp(); powerups_group.add(new_pw); all_sprites.add(new_pw)
        bg_speed = 5 + current_diff + bonus_speed
        bg_y = (bg_y + bg_speed) % HEIGHT
        distance += bg_speed * 0.1
        screen.blit(bg, (0, bg_y)); screen.blit(bg, (0, bg_y - HEIGHT))
        all_sprites.update(current_diff + bonus_speed)
        if p.has_shield: pygame.draw.circle(screen, (0, 255, 0), p.rect.center, 45, 3)
        all_sprites.draw(screen)
        score_txt = font_small.render(f"Score: {score} | Coins: {sum_coins}", True, (255, 255, 255))
        screen.blit(score_txt, (10, 10))
        dist_txt = font_small.render(f"{int(distance)} m", True, (255, 255, 255))
        screen.blit(dist_txt, (WIDTH - 120, 10))
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(s, c, d):
    btn_retry = Button("RETRY", 250, 450, 150, 50, (0, 200, 0))
    btn_menu = Button("MENU", 440, 450, 150, 50, (0, 0, 200))
    while True:
        screen.fill((150, 0, 0))
        txt = font_menu.render("GAME OVER", True, (255, 255, 255))
        info = font_small.render(f"Score: {s} | Coins: {c} | {d} m", True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 150))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 250))
        btn_retry.draw(screen); btn_menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(event.pos): return "RESTART"
                if btn_menu.is_clicked(event.pos): return "MENU"
        pygame.display.flip()

# --- ЖАҢА: Leaderboard экраны ---
def leaderboard_screen():
    global leaderboard
    btn_back = Button("BACK", WIDTH//2 - 75, 550, 150, 50, (100, 100, 100))
    while True:
        screen.fill((30, 30, 30))
        title = font_menu.render("TOP 10 PLAYERS", True, (255, 215, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Кесте тақырыптары
        header = font_small.render("Name          Score    Coins    Dist", True, (200, 200, 200))
        screen.blit(header, (150, 130))
        pygame.draw.line(screen, (255, 255, 255), (150, 170), (700, 170), 2)

        for i, entry in enumerate(leaderboard[:10]):
            name = str(entry.get('name', 'Unknown'))[:10]
            scr = str(entry.get('score', 0))
            cns = str(entry.get('coins', 0))
            dst = f"{int(entry.get('distance', 0))}m"
            
            row_txt = font_small.render(f"{i+1}. {name:<12} {scr:<8} {cns:<8} {dst}", True, (255, 255, 255))
            screen.blit(row_txt, (150, 180 + i * 35))

        btn_back.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.is_clicked(event.pos): return
        pygame.display.flip()

def main_menu():
    global leaderboard, settings
    while True:
        screen.fill((230, 230, 230))
        title = font_menu.render("RACER PRO", True, (50, 50, 50))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        btn_start = Button("START", 320, 200, 200, 50, (50, 150, 50))
        btn_leaders = Button("LEADERS", 320, 270, 200, 50, (200, 150, 0)) # Жаңа батырма
        music_txt = "MUSIC: ON" if settings["sound"] else "MUSIC: OFF"
        btn_music = Button(music_txt, 320, 340, 200, 50, (150, 150, 50))
        btn_exit = Button("EXIT", 320, 410, 200, 50, (150, 50, 50))
        
        for b in [btn_start, btn_leaders, btn_music, btn_exit]: b.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.is_clicked(event.pos):
                    u_name = get_user_name()
                    choice = "RESTART"
                    while choice == "RESTART":
                        s, c, d = game_loop()
                        leaderboard.append({"name": u_name, "score": s, "coins": c, "distance": d, "date": time.strftime("%Y-%m-%d %H:%M")})
                        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
                        save_json('leaderboard.json', leaderboard)
                        choice = game_over_screen(s, c, d)
                elif btn_leaders.is_clicked(event.pos):
                    leaderboard_screen()
                elif btn_music.is_clicked(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_json('settings.json', settings)
                    if settings["sound"]: pygame.mixer.music.play(-1)
                    else: pygame.mixer.music.stop()
                elif btn_exit.is_clicked(event.pos):
                    pygame.quit(); sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()