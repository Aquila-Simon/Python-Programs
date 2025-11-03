import pygame, sys, random

# -- Initialize Pygame --
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# -- Setting up Window Display --
WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption('Flappy Dupe')
display = pygame.Surface((800, 800))

# -- Setting Up Colours to be Used in Game --
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (65, 152, 10)
PIPE_BROWN = (164, 116, 73)
PIPE_HIT = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# -- Setting up Fonts to be used in the Game --
# -- Will need to be tested to see which sizes work best for different text elements --
font_small = pygame.font.SysFont('Rockwell', 25)
font_medium = pygame.font.SysFont('Rockwell', 40)
font_large = pygame.font.SysFont('Rockwell', 50)

# -- Game Start Variables --
ground_rect = pygame.Rect(0, 650, 800, 150)  #Rectangle for Ground
score = 0
high_score = 0
game_state = 'Start_Game'
start_game = True
player_location = [100, 0]
gravity = 0
pipe_scroll_speed = 5

# -- Player Setup --
# -- Current Player Image is a Placeholder will need to be replaced with final sprite once designed --
player_image = pygame.image.load('stephen.png').convert()
player_image.set_colorkey(WHITE)
player_rect = player_image.get_rect(topleft=(player_location[0], player_location[1]))

# -- Pipe Setup --
PIPE_WIDTH = 100
PIPE_GAP = 200
WINDOW_HEIGHT = WINDOW_SIZE[1]

# -- Creating Pipes -- 
def create_pipes():
    x_pos = 700
    # -- Randomly determine the height of the upper pipe --
    gap_y = random.randint(150, WINDOW_HEIGHT - PIPE_GAP - 150)
    # -- Create upper and lower pipe rectangles --
    top_pipe = pygame.Rect(x_pos, 0, PIPE_WIDTH, gap_y)
    bottom_pipe = pygame.Rect(x_pos, gap_y + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT - (gap_y + PIPE_GAP))

    return top_pipe, bottom_pipe

upper_pipe_rect, lower_pipe_rect = create_pipes()

# -- Other Functions and Game Logic will go here --
def reset_game():
    global player_location, gravity, score, upper_pipe_rect, lower_pipe_rect, pipe_scroll_speed
    player_location = [100, 300]
    gravity = 0
    score = 0
    pipe_scroll_speed = 5
    upper_pipe_rect, lower_pipe_rect = create_pipes()

def draw_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    display.blit(text_surface, position)

# -- Main Game Loop --
while start_game:
    # -- Handling Event Cases --
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_SPACE) and game_state == 'Playing_Game':
                gravity = -12
            elif event.key == pygame.K_RETURN:
                if game_state in ('Start_Game', 'Game_Over'):
                    game_state = 'Playing_Game'
                    reset_game()
                elif game_state == 'Pause_Game':
                    game_state = 'Playing_Game'
            elif event.key == pygame.K_ESCAPE and game_state == 'Playing_Game':
                game_state = 'Pause_Game'
    # -- Game Logic --
    if game_state == 'Playing_Game':
        display.fill(SKY_BLUE)
        pygame.draw.rect(display, GROUND_GREEN, ground_rect)

        # -- Update player position --
        gravity = min(gravity + 1, 5)
        player_location[1] += gravity
        player_rect.topleft = player_location

        # -- Move pipes --
        upper_pipe_rect.x -= pipe_scroll_speed
        lower_pipe_rect.x -= pipe_scroll_speed

        # -- Check for pipe reset and scoring --
        if upper_pipe_rect.right < player_rect.left:
            score += 1
            upper_pipe_rect, lower_pipe_rect = create_pipes()

        # -- Increase difficulty --
        pipe_scroll_speed = min(5 + score // 10, 10)

        # -- Collision Detection --
        collision = player_rect.colliderect(ground_rect) or player_rect.colliderect(upper_pipe_rect) or player_rect.colliderect(lower_pipe_rect)

        if collision:
            game_state = 'Game_Over'
            if score > high_score:
                high_score = score
        
        # -- Draw Pipes --
        for pipe in (upper_pipe_rect, lower_pipe_rect):
            color = PIPE_HIT if player_rect.colliderect(pipe) else PIPE_BROWN
            pygame.draw.rect(display, color, pipe)

        # -- Draw Player --
        display.blit(player_image, player_location)

        # -- Draw Score --
        draw_text(f'Score: {score}', font_small, WHITE, (5, 10))
        draw_text(f'High Score: {high_score}', font_small, WHITE, (600, 10))

    else:
        if game_state == 'Start_Game':
            display.fill(BLACK)
            draw_text('Press ENTER to Start', font_large, WHITE, (140, 350))
        elif game_state == 'Pause_Game':
            draw_text('Game Paused', font_large, WHITE, (230, 330))
            draw_text('Press RETURN to Resume', font_large, WHITE, (110, 380))
        elif game_state == 'Game_Over':
            display.fill(BLACK)
            draw_text('Game Over!', font_large, WHITE, (240, 300))
            draw_text('Press RETURN to Restart', font_large, WHITE, (110, 355))
            draw_text(f'Final Score: {score}', font_medium, WHITE, (260, 420))

    # -- Update Display --
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)