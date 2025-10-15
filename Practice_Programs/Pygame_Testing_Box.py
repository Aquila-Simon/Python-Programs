import pygame, sys

from pygame.locals import *
pygame.init()

pygame.display.set_caption("Test Display")
Window_Size = (1000, 1000)
screen = pygame.display.set_mode(Window_Size,0, 32) #Just creates window
display = pygame.Surface((500,500)) #Declares a actual surface to draw on
First_Box = pygame.Rect(50,50,400,400) #Rect(Left coordinate, Top Coordinate, Width, Height)
Second_Box = pygame.Rect(100,100,300,300)
Third_Box = pygame.Rect(150,150,200,200)
Fourth_Box = pygame.Rect(200,200,100,100)
Fifth_Box = pygame.Rect(225,225,50,50)


while True:
    display.fill((255,255,255)) #Fills surface "display" with the colour value of white
    pygame.draw.rect(display,(255,0,0),First_Box) #This line of code follows the requirements (Surface to draw on, colour value, the rectangle created above)
    pygame.draw.rect(display,(255,255,255), Second_Box)
    pygame.draw.rect(display,(255,0,0), Third_Box)
    pygame.draw.rect(display,(255,255,255), Fourth_Box)
    pygame.draw.rect(display,(255,0,0),Fifth_Box)

    for event in pygame.event.get(): #Allows for closing window that we generate
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    surf = pygame.transform.scale(display, Window_Size) #Scales surface to window size (Surface to scale, Window to scale to) Essentially just makes whatever we draw on surface "display" to show bigger or smaller
    screen.blit(surf, (0,0)) #Just draws scaled up "display" to the main screen
    pygame.display.update() #Constantly updates display