# import pygame
# from random import randint
# pygame.init()
# screen = pygame.display.set_mode((1365, 768))
# pygame.display.set_caption("Snake")
# clock = pygame.time.Clock()


# bg = pygame.image.load("snake\snake_bg.png")
# basy_img = pygame.image.load("snake\head.png")
# body_img = pygame.image.load("snake\snake_body.png")
# point_img = pygame.image.load("snake\point.png")


# basy_original = pygame.transform.scale(basy_img, (50, 50))
# body_original = pygame.transform.scale(body_img, (50, 50))
# point_original = pygame.transform.scale(point_img, (50, 50))
# basy = basy_original

# speed = 10
# basy_x = 682
# basy_y = 400
# point_random= (randint(70,1200),randint(70,600))
# #алма жеген кездеіг денесе қосылып отыру
# snake_body = []   
# snake_length = 1

# l_pressed = False
# r_pressed = False
# up_pressed = False
# down_pressed = False
# font = pygame.font.Font(None,50)
# score = 0
# running = True
# while running:
#     screen.blit(bg, (0, 0))
#     screen.blit(basy, (basy_x, basy_y))
#     screen.blit(point_original,point_random)
#     text = font.render("Score:" + str(score),False,(255,255,255))
#     screen.blit(text,(682,650))
#     for segment in snake_body:
#         screen.blit(body_original, (segment[0], segment[1]))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         if not l_pressed:
#             basy = pygame.transform.rotate(basy_original, 0)
#             l_pressed =True
#             r_pressed = False
#             up_pressed =False
#             down_pressed = False
#         basy_x -= speed
#     elif keys[pygame.K_RIGHT]:
#         if not r_pressed:
#             basy = pygame.transform.rotate(basy_original, 180)
#             l_pressed =False
#             r_pressed =True
#             up_pressed = False
#             down_pressed = False
#         basy_x += speed
#     elif keys[pygame.K_DOWN]:
#         if not down_pressed:
#             basy = pygame.transform.rotate(basy_original, 90)
#             l_pressed =False
#             r_pressed = False
#             up_pressed = False
#             down_pressed =True
#         basy_y += speed
#     elif keys[pygame.K_UP]:
#         if not up_pressed:
#             basy = pygame.transform.rotate(basy_original, -90)
#             l_pressed =False
#             r_pressed = False
#             up_pressed =True
#             down_pressed = False
#         basy_y -= speed
#     snake_body.append([basy_x, basy_y])
#     if ((basy_x-point_random[0])**2 + (basy_y-point_random[1])**2)**0.5 < 50:
#         score +=1
#         snake_length += 5
#         point_random= (randint(70,1200),randint(70,600))
        
#     pygame.display.flip()
#     clock.tick(30)
# pygame.quit()
import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((1365, 768))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

bg = pygame.image.load("snake\snake_bg.png")
basy_img = pygame.image.load("snake\head.png")
body_img = pygame.image.load("snake\snake_body.png")
point_img = pygame.image.load("snake\point.png")

basy_original = pygame.transform.scale(basy_img, (50, 50))
body_original = pygame.transform.scale(body_img, (50, 50))
point_original = pygame.transform.scale(point_img, (50, 50))
basy = basy_original

speed = 7
basy_x, basy_y = 682, 400
point_random = (randint(70, 1200), randint(70, 600))

snake_body = []
snake_length = 1
current_dir = "STOP" 

font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 100)
score = 0

running = True
game_over = False

while running:
    if not game_over:
        screen.blit(bg, (0, 0))
        for segment in snake_body:
            screen.blit(body_original, (segment[0], segment[1]))
        screen.blit(basy, (basy_x, basy_y))
        screen.blit(point_original, point_random)
        
        text = font.render("Score:" + str(score), False, (255, 255, 255))
        screen.blit(text, (682, 650))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_dir != "RIGHT":
                    current_dir = "LEFT"
                    basy = pygame.transform.rotate(basy_original, 0)
                elif event.key == pygame.K_RIGHT and current_dir != "LEFT":
                    current_dir = "RIGHT"
                    basy = pygame.transform.rotate(basy_original, 180)
                elif event.key == pygame.K_UP and current_dir != "DOWN":
                    current_dir = "UP"
                    basy = pygame.transform.rotate(basy_original, -90)
                elif event.key == pygame.K_DOWN and current_dir != "UP":
                    current_dir = "DOWN"
                    basy = pygame.transform.rotate(basy_original, 90)

        #infinite steps
        if current_dir == "LEFT":
            basy_x -= speed
        elif current_dir == "RIGHT":
            basy_x += speed
        elif current_dir == "UP":
            basy_y -= speed
        elif current_dir == "DOWN":
            basy_y += speed
        if current_dir != "STOP":
            snake_body.append([basy_x, basy_y])
            if len(snake_body) > snake_length:
                del snake_body[0]

        if basy_x < 0 or basy_x > 1315 or basy_y < 0 or basy_y > 718:
            game_over = True

        if ((basy_x - point_random[0])**2 + (basy_y - point_random[1])**2)**0.5 < 50:
            if score%3==0:
                speed +=2 
            score += 1
            snake_length += 1
            point_random = (randint(70, 1200), randint(70, 600))
            
    else:
        screen.fill((255, 0, 0))
        over_text = big_font.render("GAME OVER", True, (0, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(over_text, (450, 300))
        screen.blit(score_text, (550, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()