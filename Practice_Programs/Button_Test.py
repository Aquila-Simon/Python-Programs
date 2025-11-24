import pygame, sys, os

pygame.init()

# -- Added to run a change directory code for both MacOS and Windows --
platform_id = sys.platform
if platform_id == "win32":
    os.chdir('/Users/Aquil/Documents/Python_Programs/Python-Programs/Flappy_Bird_Dupe')
elif platform_id == "darwin":
    os.chdir('/Users/aquila-simon/Documents/Python_Programs/Python-Programs/Flappy_Bird_Dupe')

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

width = screen.get_width()
height = screen.get_height()

font_small = pygame.font.SysFont('Rockwell', 48)
font_large = pygame.font.SysFont('Rockwell', 65)

text = font_small.render("Test", True, color)
text_2 = font_small.render("Button", True, color)

button = pygame.Rect(300, 300, 200, 200)
action_from_button = pygame.Rect(0, 0, 100, 100)

hover_color = (23, 86, 130)
normal_color = (27, 107, 164)
# -- Background Setup --
background_img = pygame.image.load('background.png').convert()
background_img = pygame.transform.scale(background_img, (800, 800))

class Button:
    def __init__(self, name, width, height, position):
        self.name = name
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, self.rect)
        else:
            pygame.draw.rect(screen, normal_color, self.rect)

        text_surface = font_small.render(self.name, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

start_button = Button("Start Game", 360, 100, (219, 334))
settings_button = Button("Settings", 360, 100, (219, 452))
quit_button = Button("Quit Game", 360, 100, (219, 570))

while True:
    mouse = pygame.mouse.get_pos()
    screen.blit(background_img, (0,0))
    #Title Text
    title_text = font_large.render("SyntaxFlapError", True, (255,255,255))
    screen.blit(title_text, (400 - title_text.get_width()//2, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 500:
                #screen.fill((0,100,100))
            if start_button.is_clicked(mouse):
                print("Start Pressed")
                screen.fill((0,100,100))
            if settings_button.is_clicked(mouse):
                print("Settings Pressed")
                screen.fill((217,217,217))
            if quit_button.is_clicked(mouse):
                pygame.quit()
    
    start_button.draw(screen, mouse)
    settings_button.draw(screen, mouse)
    quit_button.draw(screen, mouse)

        #if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 500:
            #pygame.draw.rect(screen,(0, 200, 200),button)
        #else:
            #pygame.draw.rect(screen,(0, 100, 100),button)

    pygame.display.update()