import pygame
import sys
import random
from racer import Player, Enemy, Coin, PowerUp
from persistence import load_json, save_json
from ui import draw_text, Button, get_user_name

pygame.init()
WIDTH, HEIGHT = 840, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ресурстар
bg = pygame.image.load("assets/image/racer_bg.png")
avaria_sound = pygame.mixer.Sound("assets/sounds/avaria.mp3")
pygame.mixer.music.load("assets/sounds/music1.wav")

settings = load_json('settings.json', {"color": "up_player.png", "diff": 4, "music": True})
leaderboard = load_json('leaderboard.json', [])

if settings["music"]: pygame.mixer.music.play(-1)

def show_leaderboard():
    showing = True
    btn_back = Button("BACK", 370, 550, 100, 40)
    while showing:
        screen.fill((240, 240, 240))
        draw_text(screen, "TOP 10 PLAYERS", 40, 280, 50, (200, 0, 0))
        draw_text(screen, "NAME | KM | COINS", 25, 280, 120)
        
        y_offset = 170
        for i, entry in enumerate(leaderboard[:10]):
            txt = f"{i+1}. {entry['name']} | {entry['km']} km | {entry['coins']} coins"
            draw_text(screen, txt, 20, 250, y_offset)
            y_offset += 35

        btn_back.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and btn_back.is_clicked(event.pos):
                showing = False
        pygame.display.flip()

def game_loop():
    player = Player(f"assets/image/{settings['color']}")
    enemies, coins, powerups = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    score, sum_coin, distance, bg_y = 0, 0, 0, 0
    speed_car = settings["diff"]
    
    running = True
    while running:
        dt = clock.tick(60)
        distance += 1 # км ретінде есептеу
        
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 650))
        bg_y = (bg_y + 5) % 650

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Объектілерді шығару
        if random.randint(1, 100) == 1:
            e = Enemy("assets/image/up_car.png", speed_car)
            enemies.add(e); all_sprites.add(e)
        if random.randint(1, 120) == 1:
            c = Coin("assets/image/up_coin.png", random.randint(1, 3))
            coins.add(c); all_sprites.add(c)

        # Соқтығысу
        if pygame.sprite.spritecollideany(player, enemies):
            avaria_sound.play()
            return distance, sum_coin

        coin_hit = pygame.sprite.spritecollideany(player, coins)
        if coin_hit:
            sum_coin += coin_hit.weight
            if sum_coin % 10 == 0: speed_car += 1
            coin_hit.kill()

        all_sprites.update()
        for s in all_sprites: screen.blit(s.image, s.rect)
        
        draw_text(screen, f"KM: {distance}", 25, 10, 10)
        draw_text(screen, f"COINS: {sum_coin}", 25, 10, 45)
        pygame.display.flip()

def main_menu():
    while True:
        screen.fill((255, 255, 255))
        btn_play = Button("START", 320, 200, 200, 50, (100, 255, 100))
        btn_music = Button(f"MUSIC: {'ON' if settings['music'] else 'OFF'}", 320, 270, 200, 50)
        btn_leads = Button("LEADERBOARD", 320, 340, 200, 50, (100, 100, 255))
        
        for b in [btn_play, btn_music, btn_leads]: b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.is_clicked(event.pos):
                    km, coins = game_loop()
                    name = get_user_name(screen)
                    leaderboard.append({"name": name, "km": km, "coins": coins})
                    # Соңғы нәтижені сақтау және км бойынша сұрыптау
                    save_json('leaderboard.json', sorted(leaderboard, key=lambda x: x['km'], reverse=True))
                if btn_music.is_clicked(event.pos):
                    settings["music"] = not settings["music"]
                    if settings["music"]: pygame.mixer.music.play(-1)
                    else: pygame.mixer.music.stop()
                    save_json('settings.json', settings)
                if btn_leads.is_clicked(event.pos):
                    show_leaderboard()
        pygame.display.flip()

main_menu()