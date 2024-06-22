# This code is heavily inspired by DaFluffyPotato's Tutorials

from pygame.locals import *
import pygame
import sys

# globals
WHITE = (255, 255, 255)
GREEN = (20, 255, 140)
GREY = (210, 210, 210)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BACKGROUND = (4, 234, 220)


# pygame setup
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Pellet Ninja")
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))  # to scale the display

# animation sprite
global animation_frames
animation_frames = {}


def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 174, 201))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database = {}

animation_database["run"] = load_animation("sprites/run", [7, 7, 7])
animation_database["idle"] = load_animation("sprites/idle", [80, 3, 3])
animation_database["jump"] = load_animation("sprites/jump", [80])

# Player Attributes
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
player_rect = pygame.Rect(25, 100, 19, 24)

# Player Sprites
player_action = "idle"
player_frame = 0
player_flip = False

# Level design
game_map = [
    ["1", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "1"],
    ["5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "3"],
    ["5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "3"],
    ["5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "3"],
    ["1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "3"],
    ["5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "3"],
    ["5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2", "1"],
    ["5", "0", "0", "0", "2", "2", "2", "0", "0", "0", "0", "0", "2", "2", "2", "2", "2", "1", "1"],
    ["5", "0", "0", "0", "1", "1", "1", "0", "0", "0", "0", "2", "1", "1", "1", "1", "1", "1", "1"],
    ["5", "0", "0", "0", "1", "1", "1", "0", "0", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["5", "0", "0", "0", "1", "1", "1", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "2", "2", "2", "1", "1", "1", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
]
# Level Sprites
floor_img = pygame.image.load("sprites/tiles/floor.png")
filler_img = pygame.image.load("sprites/tiles/filler.png")
wall_R_img = pygame.image.load("sprites/tiles/wall_r.png")
wall_L_img = pygame.image.load("sprites/tiles/wall_l.png")
ceil_img = pygame.image.load("sprites/tiles/ceil.png")

# Collision Functions
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
    return rect, collision_types


while True:  # game loop
    display.fill(BACKGROUND)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == "1":
                display.blit(filler_img, (x * 16, y * 16))
            if tile == "2":
                display.blit(floor_img, (x * 16, y * 16))
            if tile == "3":
                display.blit(wall_L_img, (x * 16, y * 16))
            if tile == "4":
                display.blit(ceil_img, (x * 16, y * 16))
            if tile == "5":
                display.blit(wall_R_img, (x * 16, y * 16))
            if tile != "0":
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, "idle")
    if player_movement[0] > 0:
        player_flip = False
        if vertical_momentum < 0:
            player_action, player_frame = change_action(
                player_action, player_frame, "jump"
            )
        else:
            player_action, player_frame = change_action(
                player_action, player_frame, "run"
            )
    if player_movement[0] < 0:
        player_flip = True
        if vertical_momentum < 0:
            player_action, player_frame = change_action(
                player_action, player_frame, "jump"
            )
        else:
            player_action, player_frame = change_action(
                player_action, player_frame, "run"
            )
    if vertical_momentum < 0:
        player_action, player_frame = change_action(player_action, player_frame, "jump")

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions["bottom"] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(
        pygame.transform.flip(player_img, player_flip, False),
        (player_rect.x, player_rect.y),
    )

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
