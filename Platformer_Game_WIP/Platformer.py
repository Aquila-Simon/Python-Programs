import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Platformer Game #1')
WINDOW_SIZE = (600, 400) #Sets Window size that popsup
screen = pygame.display.set_mode(WINDOW_SIZE, 0 , 32) #Sets Window size that popsup
display = pygame.Surface((300, 200)) #Sets the screen scaled up to make the sprites bigger

grass_image = pygame.image.load('grass.png') #Sets Image for Grass and Dirt
tile_size = grass_image.get_width()
dirt_image = pygame.image.load('dirt.png')

moving_left = False #Movement Setup
moving_right = False

player_y_momentum = 0 #Gravity Setup
air_timer = 0

true_scroll = [0,0] #Camera Scroll

def load_map (path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

# Lines 38 - 70 Covers Animation of Idle and Run, can be expanded to include other animations
global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        
animation_database = {}

animation_database['run'] = load_animation(('player_animations/run'),[7,7])
animation_database['idle'] = load_animation(('player_animations/idle'),[7,7,40])

player_action = 'idle'
player_frame = 0
player_flip = False
# Lines 38 - 70 Covers Animation of Idle and Run, can be expanded to include other animations

game_map = load_map('map') #Loads map from Text File (Will be modified to create the infinite world, placeholder for now)

player_rect = pygame.Rect(100,100,5,13) #Creates the Players "Hitbox" used for Gravity at this time, can be used for health bar in other cases

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]] #Just background objects for Parallax Scrolling to add dynamic backgrounds

#Lines 80 - 107 Covers Collision and how it is proccessed
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collisions_types = {'top' : False, 'bottom' : False, "left" : False, 'right' : False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collisions_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collisions_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)   
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collisions_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collisions_types['top'] = True
    return rect, collisions_types
#Lines 80 - 107 Covers Collision and how it is proccessed

#Game Loop Starts here - Most of the actual controls and displays are controlled here
while True:
    display.fill((135,206,250)) #Sets a background colour

#Lines 115 - 119 Covers Camera Scrolling - this code allows for the camera to move fast if far from the player and slow if close to the player, it also adds a slight delay which gives it the classic platformer feel
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152)/20 
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
#Lines 115 - 119 Covers Camera Scrolling - this code allows for the camera to move fast if far from the player and slow if close to the player, it also adds a slight delay which gives it the classic platformer feel

    pygame.draw.rect(display, (7,80,75), pygame.Rect(0,120,300,80)) #Draws a horizon in the background that is static
#Lines 124 - 129 Adds in the squares in the background for the Parallax Scrolling and gives them colour
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1][1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150), obj_rect)
        else:
            pygame.draw.rect(display, (9,91,85), obj_rect)
#Lines 124 - 129 Adds in the squares in the background for the Parallax Scrolling and gives them colour

#Lines 132 - 144 Fills in the map that we generated earlier with the proper graphics and adds in Logic for Camera Scrolling        
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x*tile_size - scroll[0], y*tile_size - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x*tile_size  - scroll[0], y*tile_size - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size))
            x += 1
        y += 1
#Lines 132 - 144 Fills in the map that we generated earlier with the proper graphics and adds in Logic for Camera Scrolling     

#Lines 149 - 157 Covers Movement Logic, actual controls is further down
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
#Lines 149 - 157 Covers Movement Logic, actual controls is further down

#Lines 161 - 174 Covers Animations based on the movement of the character
    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_image_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_image_id]
    display.blit(pygame.transform.flip(player_image,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))        
#Lines 161 - 174 Covers Animations based on the movement of the character as well as how the animation is used ona frame by frame basis

#Lines 178 - 185 Covers Collision Logic
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer = 1
    if collisions['top']:
        player_y_momentum = 0.2
#Lines 178 - 185 Covers Collision Logic

#Lines 189 - 205 Covers the Logic for Inputs and Controls
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                if air_timer < 3:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
#Lines 189 - 205 Covers the Logic for Inputs and Controls

#This last bit just scales the screen to the window, updates the display constantly, and sets the frame rate to be 60 fps
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(60)