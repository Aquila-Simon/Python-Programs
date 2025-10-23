import pygame, sys, random
from pygame.locals import *
pygame.init()
pygame.font.init()

#Inital Setup
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Dupe')
WINDOW_SIZE = (800, 800) #Sets Window size that popsup
screen = pygame.display.set_mode(WINDOW_SIZE, 0 , 32) #Sets Window size that popsup
display = pygame.Surface((800, 800)) #Sets the surface for the all the game elements to be drawn on

ground_rect = pygame.Rect(0, 650, 800, 150) #Ground Rectangle

font = pygame.font.SysFont('Arial', 25) #Font for Score
score = 0 #Player Score
score_text= font.render('Score: ' + str(score), False, (255,255,255))
high_score = 0 #Player High Score
high_score_text= font.render('High Score: ' + str(high_score), False, (255,255,255))

start_game = True #Variable to control the main game loop

#Player movement variables
player_location = [100,0]
gravity = 0
Moving_Right = False
Moving_Left = False
Moving_Up = False
Moving_Down = False
air_timer = 0
upper_pipe_location = [700, 0]
lower_pipe_location = [700, 500]

player_image = pygame.image.load('stephen.png').convert() #Player Image (Placeholder for now)
player_image.set_colorkey((255,255,255))
player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height()) #Player Rectangle
Upper_pipe_rect = pygame.Rect(upper_pipe_location[0], upper_pipe_location[1], 100, 300)
Lower_pipe_rect = pygame.Rect(lower_pipe_location[0], lower_pipe_location[1], 100, 300)

#Start Sequence for Game

while start_game == True: #Main Game Loop

    display.fill((135, 206, 235)) #Fills the screen with sky blue before drawing elements (Main Background)
    pygame.draw.rect(display, (65,152,10), ground_rect) #Draws the ground
    display.blit(score_text, (0,0)) #Draws Score
    display.blit(high_score_text, (625,0)) #Draws High Score
    Upper_pipe_rect = pygame.Rect(upper_pipe_location[0], upper_pipe_location[1], 100, 300)
    Lower_pipe_rect = pygame.Rect(lower_pipe_location[0], lower_pipe_location[1], 100, 300)

    if player_rect.colliderect(Upper_pipe_rect): #Ground Collision
        pygame.draw.rect(display, (255,0,0), Upper_pipe_rect) #Draws Upper Pipe
    else:
        pygame.draw.rect(display, (164,116,73), Upper_pipe_rect) #Draws Upper Pipe
    if player_rect.colliderect(Lower_pipe_rect): #Ground Collision
        pygame.draw.rect(display, (255,0,0), Lower_pipe_rect) #Draws Lower Pipe
    else:
        pygame.draw.rect(display, (164,116,73), Lower_pipe_rect) #Draws Lower Pipe

    if player_rect.colliderect(Upper_pipe_rect): #Upper Pipe Collision
        player_location[0] = 100
        player_location[1] = 300
        upper_pipe_location[0] = 800
        lower_pipe_location[0] = 800
        score = 0
        score_text= font.render('Score: ' + str(score), False, (255,255,255))
    if player_rect.colliderect(Lower_pipe_rect): #Lower Pipe Collision
        player_location[0] = 100
        player_location[1] = 300
        upper_pipe_location[0] = 800
        lower_pipe_location[0] = 800
        score = 0
        score_text= font.render('Score: ' + str(score), False, (255,255,255))

    if player_rect.colliderect(ground_rect): #Ground Collision
        player_location[0] = 100
        player_location[1] = 300
        score = 0
        score_text= font.render('Score: ' + str(score), False, (255,255,255))
        upper_pipe_location[0] = 800
        lower_pipe_location[0] = 800


    player_location[1] += gravity
    gravity += 1
    if gravity > 5:
        gravity = 5

    display.blit(player_image, player_location) #Draws the player image
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]
    upper_pipe_location[0] -= 5
    lower_pipe_location[0] -= 5

    display.blit(score_text, (0,0)) #Draws Score
    display.blit(high_score_text, (625,0)) #Draws High Score

    if (upper_pipe_location[0] + 100) < player_location[0]: #Score Increase and Pipe Reset
        score += 1
        score_text= font.render('Score: ' + str(score), False, (255,255,255))
        upper_pipe_location[0] = 800
        lower_pipe_location[0] = 800
    if score > high_score:
        high_score = score
        high_score_text= font.render('High Score: ' + str(high_score), False, (255,255,255))

    for event in pygame.event.get(): #Event Loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_SPACE: #Jump/Flap
                gravity = -12
            if event.key == K_ESCAPE: #Quit Game
                display.fill((0,0,0))
                start_game = False
                if event.type == K_r:
                    high_score = 0 #Player High Score
                    high_score_text= font.render('High Score: ' + str(high_score), False, (255,255,255))

    #Draws main surface to the display
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60) #sets framerate to 60 fps