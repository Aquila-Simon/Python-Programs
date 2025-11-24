import pygame, sys, random, math, os

# -- Added to run a change directory code for both MacOS and Windows --
platform_id = sys.platform
if platform_id == "win32":
    os.chdir('/Users/Aquil/Documents/Python_Programs/Python-Programs/Flappy_Bird_Dupe')
elif platform_id == "darwin":
    os.chdir('/Users/aquila-simon/Documents/Python_Programs/Python-Programs/Flappy_Bird_Dupe')

# -- Initialize Pygame --
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# -- Setting up Window Display --
WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption('SyntaxFlapError')
display = pygame.Surface(WINDOW_SIZE)

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
font_large = pygame.font.SysFont('Rockwell', 65) #Best for Titles
font_button = pygame.font.SysFont('Rockwell', 48) #Button Text


# -- Game Start Variables --
ground_rect = pygame.Rect(0, 650, 800, 150)  #Rectangle for Ground
ground_y = 650
ground_height = 150
score = 0
high_score = 0
game_state = 'Start_Game'
start_game = True
player_location = [100, 0]
gravity = 0
gravity_acceleration = 0.6
flap_strength = -11
max_fall_speed = 10
peak_flap_factor = 0.8
pipe_scroll_speed = 5
collision_flash_timer = 0
ground_scroll = 0
scroll_speed = 5  # tweak for smoother motion
background_scroll = 0
background_speed = 2  # slower than ground and pipes for depth

# -- Player Rotation Variables --
player_angle = 0
max_up_angle = 25
max_down_angle = -80
tilt_speed = 3

# -- Player Setup --
# -- Current Player Image is a Placeholder will need to be replaced with final sprite once designed --
player_image = pygame.image.load('stephen.png').convert()
player_image.set_colorkey(WHITE)
player_rect = player_image.get_rect(topleft=(player_location[0], player_location[1]))

# -- Ground Setup --
ground_image = pygame.image.load('ground.png')

# -- Pipe Setup --
pipe_top_img = pygame.image.load('pipe_top.png')
pipe_body_img = pygame.image.load('pipe_body.png')

# -- Background Setup --
background_img = pygame.image.load('background.png').convert()
background_img = pygame.transform.scale(background_img, (800, 800))

def draw_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    display.blit(text_surface, position)

# -- Button Setup --
hover_color = (23, 86, 130)
normal_color = (27, 107, 164)

# -- Class for defining button --
class Button:
    def __init__(self, name, width, height, position):
        self.name = name
        self.rect = pygame.Rect(position[0], position[1], width, height)

    # -- Draws Button and Text on Button --
    # -- Might Require some Tweaking once Integrated, mostly for text centering --
    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, self.rect)
        else:
            pygame.draw.rect(screen, normal_color, self.rect)

        text_surface = font_button.render(self.name, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    # -- Checks if Button was clicked
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# -- Start Screen Revamp --
def draw_start_screen():
    display.blit(background_img, (0,0)) #Draws background onto start screen

    #Title Text
    title_text = font_large.render("SyntaxFlapError", True, (WHITE))
    display.blit(title_text, (400 - title_text.get_width()//2, 200))
    display.blit(player_image, (375, 375))
    #Press Space Prompt
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        prompt_text = font_small.render("Press ENTER to Start", True, (WHITE))
        display.blit(prompt_text, (400 - prompt_text.get_width()//2, 550))

# -- Fade to white test before game starts --
def fade_to_white(surface, duration_frames=30):
    fade_surface = pygame.Surface(WINDOW_SIZE)
    fade_surface.fill((WHITE))

    for alpha in range(0, 256, int(256/duration_frames)):
        fade_surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    
    fade_surface.set_alpha(255)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip
    clock.tick(60)

# -- Game Over Screen Revamp -- (Decide if we want High Score and Score or only Score??)
def draw_game_over():
    display.blit(background_img, (0,0))

    #Fade to Black overlay
    overlay = pygame.Surface(WINDOW_SIZE)
    overlay.set_alpha(160)
    overlay.fill((BLACK))
    display.blit(overlay, (0,0))

    #Title Text
    title = font_large.render("Game Over!", True, (WHITE))
    display.blit(title, (400 - title.get_width()//2, 200))
    #Current Score
    score_text = font_medium.render(f"Score: {score}", True, (WHITE))
    display.blit(score_text, (400 - score_text.get_width()//2, 320))
    #High Score (Not Sure if we should show?)
    high_score_text = font_medium.render(f"High Score: {high_score}", True, (WHITE))
    display.blit(high_score_text, (400 - high_score_text.get_width()//2, 380))

    #Restart Game Prompt
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        prompt = font_small.render("Press RETURN to Restart", True, (WHITE))
        display.blit(prompt, (400 - prompt.get_width()//2, 500))

# -- Pipe Setup --
PIPE_WIDTH = 100
PIPE_GAP = 190
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

# -- Multiple Pipe Setup --
pipes = []
PIPE_SPAWN_FREQUENCY = 1400  # milliseconds
last_pipe_spawn_time = pygame.time.get_ticks()
pause_start_time = None

def add_pipe_pair():
    top, bottom = create_pipes()
    pipes.append({'top': top, 'bottom': bottom, 'scored': False})

# -- Debug Overlay Variables --
debug_mode = False
debug_font = pygame.font.SysFont('Consolas', 20)

def draw_debug_overlay(display, player_rect, pipes, clock):
    """Draws FPS, hitboxes, spacing grid, and pipe spawn/gap guides with a soft fade pulse."""
    time_now = pygame.time.get_ticks()
    # Alpha pulse between 60 and 120
    pulse_alpha = 60 + int(60 * (math.sin(time_now * 0.004) + 1) / 2)

    # Create semi-transparent surface
    overlay = pygame.Surface((800, 800), pygame.SRCALPHA)

    # -- Semi-transparent ground grid --
    grid_color = (80, 80, 80, pulse_alpha)
    for y in range(0, 800, 50):  # horizontal grid lines every 50px
        pygame.draw.line(overlay, grid_color, (0, y), (800, y), 1)
    for x in range(0, 800, 100):  # vertical lines every 100px
        pygame.draw.line(overlay, grid_color, (x, 0), (x, 800), 1)

    # -- Pipe spawn reference line (x = 700) --
    pygame.draw.line(overlay, (255, 255, 255, min(pulse_alpha + 40, 180)), (700, 0), (700, 800), 2)

    # -- Pipe gap centerlines --
    for pipe_pair in pipes:
        top = pipe_pair['top']
        bottom = pipe_pair['bottom']
        gap_center_y = top.bottom + (bottom.top - top.bottom) // 2
        pygame.draw.line(overlay, (0, 255, 255, min(pulse_alpha + 40, 180)), (top.left, gap_center_y), (top.right, gap_center_y), 2)

    # -- Apply overlay --
    display.blit(overlay, (0, 0))

    # -- FPS counter --
    fps_text = debug_font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 0))
    display.blit(fps_text, (10, 40))

    # -- Debug mode label --
    status_text = debug_font.render("DEBUG ON", True, (255, 100, 100))
    display.blit(status_text, (680, 10))

    # -- Player hitbox --
    pygame.draw.rect(display, (0, 255, 0), player_rect, 2)

    # -- Pipe hitboxes --
    for pipe_pair in pipes:
        pygame.draw.rect(display, (255, 255, 0), pipe_pair['top'], 2)
        pygame.draw.rect(display, (255, 255, 0), pipe_pair['bottom'], 2)

# -- Other Functions and Game Logic will go here --
def reset_game():
    global player_location, gravity, score, pipe_scroll_speed
    global pipes, last_pipe_spawn_time
    global collision_flash_timer
    global ground_scroll

    player_location = [100, 300]
    gravity = 0
    score = 0
    pipe_scroll_speed = 5
    collision_flash_timer = 0
    ground_scroll = 0

    # Reset pipe system
    pipes = []
    add_pipe_pair()
    last_pipe_spawn_time = pygame.time.get_ticks()

# -- Main Game Loop --
while start_game:
    # -- Handling Event Cases --
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_SPACE) and game_state == 'Playing_Game':
                gravity = flap_strength
            elif event.key == pygame.K_RETURN:
                if game_state in ('Start_Game', 'Game_Over'):
                    fade_to_white(display)
                    game_state = 'Playing_Game'
                    reset_game()
                elif game_state == 'Pause_Game':
                    # When unpausing, adjust pipe spawn timer to ignore pause duration
                    if pause_start_time is not None:
                        paused_duration = pygame.time.get_ticks() - pause_start_time
                        last_pipe_spawn_time += paused_duration
                        pause_start_time = None
                    game_state = 'Playing_Game'
            elif event.key == pygame.K_ESCAPE and game_state == 'Playing_Game':
            # When pausing, record the pause start time
                pause_start_time = pygame.time.get_ticks()
                game_state = 'Pause_Game'
            elif event.key == pygame.K_ESCAPE and game_state == 'Game_Over': #For Easier exiting when game is over
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_ESCAPE and game_state == 'Pause_Game': #For Easier exiting when game is paused
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RALT:
                debug_mode = not debug_mode # -- Toggles Debug Mode --
    # -- Game Logic --
    if game_state == 'Playing_Game':
        display.fill(SKY_BLUE)
        pygame.draw.rect(display, (65,152,10), ground_rect) #Draws the ground

        # -- Update background scroll --
        background_scroll -= background_speed
        if abs(background_scroll) > 800:
            background_scroll = 0

        # -- Update player position --
        gravity = min(gravity + gravity_acceleration, max_fall_speed)
        if -2 < gravity < 0:
            gravity *= peak_flap_factor
        player_location[1] += gravity
        player_rect.topleft = player_location

        # -- Update player rotation --
        if gravity < 0:
            player_angle = max_up_angle # -- Tilt Up --
        else:
            player_angle = max(player_angle - tilt_speed, max_down_angle) # -- Tilt Down --

        # -- Update ground scroll --
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 800:
            ground_scroll = 0

        # -- Spawn New Pipes --
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_spawn_time > PIPE_SPAWN_FREQUENCY:
            add_pipe_pair()
            last_pipe_spawn_time = current_time

        # -- Draw Parallax Background --
        display.blit(background_img, (background_scroll, 0))
        display.blit(background_img, (background_scroll + 800, 0))

        # -- Move Pipes and Check for Scoring --
        bird_center_x = player_rect.centerx
        for pipe_pair in pipes:
            top_pipe = pipe_pair['top']
            bottom_pipe = pipe_pair['bottom']

            # -- Move Pipes --
            top_pipe.x -= pipe_scroll_speed
            bottom_pipe.x -= pipe_scroll_speed

            # -- Scoring Functionality --
            pipe_center_x = top_pipe.centerx
            if not pipe_pair['scored'] and pipe_center_x < bird_center_x:
                score += 1
                pipe_pair['scored'] = True
            # -- Remove Off-Screen Pipes --
            if top_pipe.right < 0:
                pipes.remove(pipe_pair)

        # -- Draw Pipes --
        for pipe_pair in pipes:
            top_rect = pipe_pair['top']
            bottom_rect = pipe_pair['bottom']

            # Optional: keep rect for debug visualization
            color_top = PIPE_HIT if player_rect.colliderect(top_rect) else PIPE_BROWN
            color_bottom = PIPE_HIT if player_rect.colliderect(bottom_rect) else PIPE_BROWN
            # Comment out these two if you don’t want the colored rectangles visible
            # pygame.draw.rect(display, color_top, top_rect)
            # pygame.draw.rect(display, color_bottom, bottom_rect)

            # --- Draw pipe images ---
            # Scale body images to fit rects
            top_body_scaled = pygame.transform.scale(pipe_body_img, (top_rect.width, top_rect.height))
            bottom_body_scaled = pygame.transform.scale(pipe_body_img, (bottom_rect.width, bottom_rect.height))

            # Flip the top pipe image vertically (so it’s upside-down)
            top_body_scaled = pygame.transform.flip(top_body_scaled, False, True)

            # Draw images at rect positions
            display.blit(top_body_scaled, (top_rect.x, top_rect.y))
            display.blit(bottom_body_scaled, (bottom_rect.x, bottom_rect.y))

            # Optional: if you have a separate cap/lip image, draw it here
            # display.blit(pipe_top_img, (top_rect.x, top_rect.bottom - pipe_top_img.get_height()))
            # display.blit(pipe_top_img, (bottom_rect.x, bottom_rect.y))

        # -- Increase difficulty --
        pipe_scroll_speed = min(5 + score // 10, 10)

        # -- Collision Detection --
        collision = player_rect.colliderect(ground_rect) or any(player_rect.colliderect(pipe_rect)
        for pipe_pair in pipes
            for pipe_rect in (pipe_pair['top'], pipe_pair['bottom'])
        )
        if collision:
            game_state = 'Game_Over'
            collision_flash_timer = 30
            if score > high_score:
                high_score = score

        # -- Draw Scrolling Ground --
        display.blit(ground_image, (ground_scroll,ground_y))
        display.blit(ground_image, (ground_scroll + 800, ground_y))

        # -- Draw Player --
        rotated_bird = pygame.transform.rotozoom(player_image, player_angle, 1.0)
        rotated_rect = rotated_bird.get_rect(center=player_rect.center)
        display.blit(rotated_bird, rotated_rect)

        # -- Draw Score --
        draw_text(f'Score: {score}', font_small, WHITE, (5, 10))
        draw_text(f'High Score: {high_score}', font_small, WHITE, (600, 10))

        # -- Collision Flash Effect --
        if collision_flash_timer > 0:
            flash_surface = pygame.Surface((800, 800))
            flash_surface.set_alpha(int(150 * (collision_flash_timer / 30)))  # fade out
            flash_surface.fill((255, 0, 0))
            display.blit(flash_surface, (0, 0))
            collision_flash_timer -= 1

        # -- Debug Overlay --
        if debug_mode:
            draw_debug_overlay(display, player_rect, pipes, clock)

    else:
        if game_state == 'Start_Game':
            #display.fill(BLACK)
            #draw_text('Press ENTER to Start', font_large, WHITE, (140, 350))
            draw_start_screen()
        elif game_state == 'Pause_Game':
            draw_text('Game Paused', font_large, WHITE, (230, 330))
            draw_text('Press RETURN to Resume', font_large, WHITE, (110, 380))
        elif game_state == 'Game_Over':
            #display.fill(BLACK)
            #draw_text('Game Over!', font_large, WHITE, (240, 300))
            #draw_text('Press RETURN to Restart', font_large, WHITE, (110, 355))
            #draw_text(f'Final Score: {score}', font_medium, WHITE, (260, 420))
            draw_game_over()

    # -- Update Display --
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)