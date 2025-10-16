import pygame, sys

from pygame.locals import *
pygame.init()

Windows_Path = "Python-Programs/Practice_Programs/" # Just sets the path to the correct one based on what I was working on
pygame.display.set_caption("Test Display")
pygame.display.set_icon(pygame.image.load(Windows_Path + 'icon.jpg')) #Sets Icon for Window
Window_Size = (600, 400)
screen = pygame.display.set_mode(Window_Size,0, 32) #Just creates window
display = pygame.Surface((300,200)) #Declares a actual surface to draw on
cloud = pygame.image.load(Windows_Path + 'cloud.png') #Loads Image for cloud
#First_Box = pygame.Rect(50,50,400,400) #Rect(Left coordinate, Top Coordinate, Width, Height)
#Second_Box = pygame.Rect(100,100,300,300)
#Third_Box = pygame.Rect(150,150,200,200)
#Fourth_Box = pygame.Rect(200,200,100,100)
#Fifth_Box = pygame.Rect(225,225,50,50)
small_cloud = pygame.transform.scale(cloud, (50,24)) #Scales cloud image down to 50 width and 24 height
cloud_rect = pygame.Rect(100,100,small_cloud.get_width(),small_cloud.get_height()) #Creates rectangle based on the size of the scaled down cloud image

moving_left = False
moving_right = False
player_y_momentum = 0

while True:
    display.fill((3, 207, 252)) #Fills surface "display" with the colour value of white
    display.blit(small_cloud, (25,25)) #Draws cloud image onto surface "display" at coordinates (25,25)
    #pygame.draw.rect(display,(255,0,0),First_Box) #This line of code follows the requirements (Surface to draw on, colour value, the rectangle created above)
    #pygame.draw.rect(display,(255,255,255), Second_Box)
    #pygame.draw.rect(display,(255,0,0), Third_Box)
    #pygame.draw.rect(display,(255,255,255), Fourth_Box)
    #pygame.draw.rect(display,(255,0,0),Fifth_Box)

    for event in pygame.event.get(): #Allows for closing window that we generate
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    surf = pygame.transform.scale(display, Window_Size) #Scales surface to window size (Surface to scale, Window to scale to) Essentially just makes whatever we draw on surface "display" to show bigger or smaller
    screen.blit(surf, (0,0)) #Just draws scaled up "display" to the main screen
    pygame.display.update() #Constantly updates display