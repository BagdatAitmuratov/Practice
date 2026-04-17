import pygame 
import os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Music")
icon = pygame.image.load('bg_songs/bg_music.png')
pygame.display.set_icon(icon) 

#playlist
song_dir='songs'
songs = [music for music in os.listdir(song_dir) if music.endswith(('.mp3','.wav'))]
text = pygame.font.SysFont(None,50)
now = 0
playing= False
if songs:
    pygame.mixer.music.load(os.path.join(song_dir,songs[now]))


#art the playlists
def albom_art(song_name):
    image_name = song_name.replace('.mp3','.jpg').replace('.wav','.png')
    image_path=os.path.join('bg_songs',image_name)
    if os.path.exists(image_path):
        img = pygame.image.load(image_path)
        return pygame.transform.scale(img,(400,400))
    else:
        return icon

current_art = albom_art(songs[now])
#running music name
text_x=1000
speed = 1

runnig = True
while runnig:
    screen.fill((255,255,255))
    screen.blit(current_art, (50, 50))
    song_name = songs[now]
    text_face = text.render(f"Song:[{song_name}]" , True ,(0,0,0))
    screen.blit(text_face,(600,300))
    conntrol = pygame.font.Font(None,40)
    controlling = conntrol.render("P = Play \nS = Stop \nN = Next track \nB = Previous (Back)",True,(0,0,0))
    screen.blit(controlling,(600,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig =False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not playing:
                     pygame.mixer.music.play()
                     playing = True
                else:
                     pygame.mixer.music.unpause()
            elif event.key == pygame.K_n: # Next
                now = (now + 1) % len(songs)
                pygame.mixer.music.load(os.path.join(song_dir, songs[now]))
                pygame.mixer.music.play()
                current_art = albom_art(songs[now])
                playing = True

            elif event.key == pygame.K_b:
                now = (now - 1) % len(songs)
                pygame.mixer.music.load(os.path.join(song_dir, songs[now]))
                pygame.mixer.music.play()
                current_art = albom_art(songs[now])
                playing = True
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                playing = False
    text_x -= speed
    if text_x < -text_face.get_width():
        text_x=1000
    pygame.draw.rect(screen,(0,0,0),(0,1000,540,60))
    screen.blit(text_face, (text_x, 555))



    pygame.display.flip()
pygame.quit()