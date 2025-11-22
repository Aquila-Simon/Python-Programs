import pygame, sys

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

width = screen.get_width()
height = screen.get_height()

font_small = pygame.font.SysFont('Rockwell', 35)

text = font_small.render("Test", True, color)
text_2 = font_small.render("Button", True, color)

button = pygame.Rect(300, 300, 200, 200)
action_from_button = pygame.Rect(0, 0, 100, 100)

hover_color = (0,200,200)
normal_color = (0, 100, 100)

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

start_button = Button("Start", 200, 200, (300, 300))

while True:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 500:
                #screen.fill((0,100,100))
            if start_button.is_clicked(mouse):
                screen.fill((0,100,100))
        else:
                screen.fill((60, 25, 60))

        
    start_button.draw(screen, mouse)

        #if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 500:
            #pygame.draw.rect(screen,(0, 200, 200),button)
        #else:
            #pygame.draw.rect(screen,(0, 100, 100),button)

    pygame.display.update()