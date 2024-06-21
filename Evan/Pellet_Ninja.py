import pygame
import random
import sys
from Pellet import *
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

# Animation functions
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


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Load the image for the player character.
        # "convert_alpha" reduces lag during the game.
        self.image = pygame.image.load("code/sprites/idle/idle_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (57, 72))

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.room = None

        # Track the direction the player is facing
        self.facing = 1

        self._health = 3

    def take_damage(self):
        self._health -= 1

    def restore(self):
        self._health = 3

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.tile_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # Otherwise if we are moving left, do the opposite.
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.tile_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # Move down a pixel and see if there is a tile below us.
        self.rect.y += 1
        tile_hit_list = pygame.sprite.spritecollide(self, self.room.tile_list, False)
        self.rect.y -= 1

        # If it is ok to jump, set our speed upwards
        if len(tile_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0



class Tile(pygame.sprite.Sprite):
    """ Tile the user can jump on """

    def __init__(self, image):
        """ Tile constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()


class Key(pygame.sprite.Sprite):
    """ The player collects the key to unlock the door. """

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("images/key.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = self.x, self.y


class MovingPlatform(Tile):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    room = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        if self.rect.x < self.boundary_left or self.rect.x > self.boundary_right:
            self.change_x *= -1

class Enemy(Tile):
    """Moving platform that damages on touch and disappears when shot"""
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    _facing = -1
    shotFrequency = 80
    jumpFrequency = 100
    shootTickCount = 0
    # need two flags to determine when to flip image
    flipFlag1 = False
    flipFlag2 = False
    pellet_list = pygame.sprite.Group()
    player = None



    room = None

    def update(self):

        if self.shootTickCount >= self.shotFrequency:
            pel = self.shoot()
            self.pellet_list.add(pel)
            self.shootTickCount = 0
        self.shootTickCount += 1

        if self.player.rect.x <= self.rect.x:
            self._facing = -1

        else:
            self._facing = 1

        # This is to determine if the enemy's image should flip
        # if the player has been on one and is now on the other, flip image
        if self.player.rect.x <= self.rect.x:
            self.flipFlag1 = True
            if self.flipFlag2:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipFlag2 = False
                self.flipFlag1 = False
        if self.player.rect.x >= self.rect.x:
            self.flipFlag2 = True
            if self.flipFlag1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipFlag2 = False
                self.flipFlag1 = False


        self.rect.x += self.change_x

        # See if we hit the player
        touched = pygame.sprite.collide_rect(self, self.player)

        if touched:
            self.player.take_damage()

            if self.change_x < 0:
                self.player.rect.right = self.player.rect.right - 50
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.player.rect.left + 50

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top - 50
            else:
                self.player.rect.top = self.rect.bottom + 50

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        if self.rect.x < self.boundary_left or self.rect.x > self.boundary_right:
            self.change_x *= -1

    def shoot(self):
        pel = Pellet(self.rect.x + (40 * self._facing) + 7, self.rect.y + 12, self._facing, "enemy_pellet")
        return pel

    def take_damage(self):
        pygame.sprite.Sprite.kill(self)
        return 0


class Boss(Enemy):
    _health = 10
    shootPhase = 0
    def __init__(self,image):

        super().__init__(image)

    def take_damage(self):
        self._health -= 1
        return self._health

    def shoot(self):
        """Slightly edited shoot, makes it so the pellet is shot at a random height"""
        if self.shootPhase == 0:
            bullet_height_mod = 60
        if self.shootPhase == 1:
            bullet_height_mod = 30
        if self.shootPhase == 2:
            bullet_height_mod = 0
            self.shootPhase = -1
        self.shootPhase += 1

        pel = Pellet(self.rect.x + (40 * self._facing) + 7, self.rect.y + bullet_height_mod, self._facing, "enemy_pellet")
        return pel




class Door(pygame.sprite.Sprite):
    """ The player reaches the unlocked door to advance to
        the next room. """

    def __init__(self, x, y):
        super().__init__()

        self.closed_image = pygame.image.load("images/closed_door.jpg").convert_alpha()
        self.closed_image = pygame.transform.scale(self.closed_image, (80, 80))
        self.open_image = pygame.image.load("images/open_door.jpg").convert_alpha()
        self.open_image = pygame.transform.scale(self.open_image, (80, 80))
        self.image = self.closed_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Room(object):
    """ This is a generic super-class used to define a room.
        Create a child class for each room with room-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            tiles collide with the player. """
        self.tile_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.key = Key(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.door = Door(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.object_list = pygame.sprite.Group()
        self.object_list.add(self.key)
        self.object_list.add(self.door)
        self.player = player
        self.player_x, self.player_y = 0, 0

        # Background image
        self.background = pygame.Surface([1200, 720])
        self.background.fill((4, 234, 220))

    # Update everything on this room
    def update(self):
        """ Update everything in this room."""
        self.tile_list.update()

        self.enemy_list.update()

        self.object_list.update()
    def draw(self, screen):
        """ Draw everything on this room. """

        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw all the sprite lists that we have
        self.tile_list.draw(screen)
        self.enemy_list.draw(screen)
        self.object_list.draw(screen)


# Create tiles for the room
class Room_1_1(Room):
    """ Definition for room 1. """

    def __init__(self, player):
        """ Create room 1. """

        # Call the parent constructor
        Room.__init__(self, player)

        # Level design
        game_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 5, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # Go through the array above and add tiles
        y = 0
        for layer in game_map:
            x = 0

            for num in layer:
                if num != 0:
                    if num == 1:
                        block = Tile(filler_img)
                    if num == 2:
                        block = Tile(floor_img)
                    if num == 3:
                        block = Tile(wall_L_img)
                    if num == 4:
                        block = Tile(ceil_img)
                    if num == 5:
                        block = Tile(wall_R_img)
                    block.rect.x, block.rect.y = x * 48, y * 48
                    block.player = self.player
                    self.tile_list.add(block)

                x += 1
            y += 1

        self.restore()
        # Place the player, key, and door
        self.player_x, self.player_y = 234, 586
        self.key.x, self.key.y = 850, 218
        self.door.rect.x, self.door.rect.y = 224, 208

    def restore(self):
        block_1 = Enemy(enemy_img)
        block_1.rect.x = 710
        block_1.rect.y = 360
        block_1.boundary_left = 710
        block_1.boundary_right = 890
        block_1.change_x = 1
        block_1.player = self.player
        block_1.room = self
        block_1.image = pygame.transform.flip(block_1.image, True, False)
        self.enemy_list.add(block_1)

# Create tiles for the room
class Room_2_1(Room):
    """ Definition for room 2. """

    def __init__(self, player):
        """ Create room 2. """

        # Call the parent constructor
        Room.__init__(self, player)

        # Level design
        game_map = [
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3],
            [5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 3],
            [5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 3],
            [5, 4, 4, 0, 0, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        ]

        # Go through the array above and add tiles
        y = 0
        for layer in game_map:
            x = 0
            for num in layer:
                if num != 0:
                    if num == 1:
                        block = Tile(filler_img)
                    if num == 2:
                        block = Tile(floor_img)
                    if num == 3:
                        block = Tile(wall_L_img)
                    if num == 4:
                        block = Tile(ceil_img)
                    if num == 5:
                        block = Tile(wall_R_img)
                    block.rect.x, block.rect.y = x * 48, y * 48
                    block.player = self.player
                    self.tile_list.add(block)
                x += 1
            y += 1

        block_1 = MovingPlatform(plat_img)
        block_1.rect.x = 700
        block_1.rect.y = 550
        block_1.boundary_left = 700
        block_1.boundary_right = 1000
        block_1.change_x = 1
        block_1.player = self.player
        block_1.room = self

        self.tile_list.add(block_1)

        # enemyp
        # Add a custom moving platform
        block_2 = MovingPlatform(plat_img)
        block_2.rect.x = 1100
        block_2.rect.y = 400
        block_2.boundary_top = 250
        block_2.boundary_bottom = 500
        block_2.change_y = 1
        block_2.player = self.player
        block_2.room = self
        self.tile_list.add(block_2)

        self.restore()
        # Place the player, key, and door
        self.player_x, self.player_y = 90, 636
        self.key.x, self.key.y = 1000,150
        self.door.rect.x, self.door.rect.y = 50, 160


    def restore(self):
        """Nothing here"""


class Room_Boss(Room):
    """ Definition for boss room. """

    def __init__(self, player):
        """ Create boss room. """

        # Call the parent constructor
        Room.__init__(self, player)

        # Level design
        game_map = [
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3],
            [5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        ]

        # Go through the array above and add tiles
        y = 0
        for layer in game_map:
            x = 0
            for num in layer:
                if num != 0:
                    if num == 1:
                        block = Tile(filler_img)
                    if num == 2:
                        block = Tile(floor_img)
                    if num == 3:
                        block = Tile(wall_L_img)
                    if num == 4:
                        block = Tile(ceil_img)
                    if num == 5:
                        block = Tile(wall_R_img)
                    block.rect.x, block.rect.y = x * 48, y * 48
                    block.player = self.player
                    self.tile_list.add(block)
                x += 1
            y += 1

        self.restore()

        self.player_x, self.player_y = 90, 636

        self.door.rect.x, self.door.rect.y = 90, 592

    def restore(self):
        boss = Boss(boss_img)
        boss.rect.x = 700
        boss.rect.y = 575
        boss.boundary_left = 700
        boss.boundary_right = 950
        boss.change_x = 1
        boss.player = self.player
        boss.room = self
        boss.image = pygame.transform.flip(boss.image, True, False)
        self.boss = boss
        self.enemy_list.add(boss)

class Button():

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self, screen, font_size, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def moused_over(self):
        # pos is the mouse position or a tuple of (x, y) coordinates
        if pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[0] < self.x + self.width:
            if pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1] < self.y + self.height:
                return True
        return False


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pellet Knight")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Load the tile images
    global floor_img, filler_img, wall_R_img, wall_L_img, ceil_img, plat_img, enemy_img, boss_img
    floor_img = pygame.image.load("code/sprites/tiles/floor.png").convert_alpha()
    floor_img = pygame.transform.scale(floor_img, (48, 48))
    filler_img = pygame.image.load("code/sprites/tiles/filler.png").convert_alpha()
    filler_img = pygame.transform.scale(filler_img, (48, 48))
    wall_R_img = pygame.image.load("code/sprites/tiles/wall_r.png").convert_alpha()
    wall_R_img = pygame.transform.scale(wall_R_img, (48, 48))
    wall_L_img = pygame.image.load("code/sprites/tiles/wall_l.png").convert_alpha()
    wall_L_img = pygame.transform.scale(wall_L_img, (48, 48))
    ceil_img = pygame.image.load("code/sprites/tiles/ceil.png").convert_alpha()
    ceil_img = pygame.transform.scale(ceil_img, (48, 48))
    plat_img = pygame.image.load("code/sprites/tiles/floor.png").convert_alpha()
    plat_img = pygame.transform.scale(floor_img, (50
                                                  , 20))
    enemy_img = pygame.image.load("code/sprites/idle/enemy.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (57, 72))
    boss_img = pygame.image.load("code/sprites/idle/Working.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (78, 96))


    # Create the player
    player = Player()

    # Sort the rooms into levels
    level_list = [[Room_1_1(player)], [Room_2_1(player)],[Room_Boss(player)]]

    # Define the buttons to be loaded later
    Title = Button((128, 255, 128), 275, 100, 600, 200, "Pellet Ninja")
    Button_1 = Button((128, 255, 128), 300, 420, 150, 150, "Level 1")
    Button_2 = Button((128, 255, 128), 500, 420, 150, 150, "Level 2")
    Button_3 = Button((128, 255, 128),700,420,150,150, "Boss")
    Game_Over = Button((128, 255, 128), 275, 100, 600, 200, "Pellet Ninja Slain!")
    Try_again = Button((128, 255, 128),330,320,500,100, "Try_Again?")
    Warning = Button((128, 255, 128), 275, 620, 600, 50, "Don't touch enemies or be shot 3 times!")
    died = False
    # Start the game
    while True:

        # If the player died, display game_over menu
        if died:
            Game_Over.draw_button(screen, 80, True)
            Try_again.draw_button(screen, 60, True)
            pygame.display.update()
            try_again = False
            while not try_again:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if Try_again.moused_over():
                            try_again = True
                            died = False

        # Load the menu so the player can choose a level
        screen.fill((128, 128, 255))
        Title.draw_button(screen, 120, True)
        Button_1.draw_button(screen, 60, True)
        Button_2.draw_button(screen, 60, True)
        Button_3.draw_button(screen,60,True)
        Warning.draw_button(screen,40,True)
        pygame.display.update()

        chosen_level = -1
        while chosen_level == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Button_1.moused_over():
                        chosen_level = 0
                    if Button_2.moused_over():
                        chosen_level = 1
                    if Button_3.moused_over():
                        chosen_level = 2

        # Set up the first room of the chosen level
        current_room_no = 0
        room_list = level_list[chosen_level]
        current_room = room_list[current_room_no]

        active_sprite_list = pygame.sprite.Group()
        player.room = current_room

        if player.facing == -1:
            player.facing = 1
            player.image = pygame.transform.flip(player.image, True, False)
        player.rect.x, player.rect.y = current_room.player_x, current_room.player_y
        player.change_x = 0
        player.change_y = 0
        active_sprite_list.add(player)

        pellet_list = pygame.sprite.Group()
        enemy_pellet_list = pygame.sprite.Group()


        current_room.key.rect.x, current_room.key.rect.y = current_room.key.x, current_room.key.y
        current_room.door.image = current_room.door.closed_image

        # -------- Main Program Loop -----------
        level_done = False
        room_done = False
        while not level_done:
            if chosen_level == 2:
                if len(current_room.enemy_list) == 0:
                    current_room.door.image = current_room.door.open_image



            for pellet in pellet_list:
                shouldDel = pellet.move(current_room.tile_list, current_room.enemy_list, "p")
                if shouldDel:
                    del pellet


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                        if player.facing == 1:
                            player.facing = -1
                            player.image = pygame.transform.flip(player.image, True, False)
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                        if player.facing == -1:
                            player.facing = 1
                            player.image = pygame.transform.flip(player.image, True, False)
                    if event.key == pygame.K_UP:
                        player.jump()
                    if event.key == pygame.K_SPACE:
                        if len(pellet_list.sprites()) < 5:
                            pellet_list.add(
                                Pellet(player.rect.x + (40 * player.facing) + 7, player.rect.y + 12, player.facing, "pellet"))

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

            if player._health <= 0:
                room_done = True
                died = True
                for enemy in current_room.enemy_list:
                    enemy.kill()
        # ending

            # Update the player.
            active_sprite_list.update()

            # Update items in the room
            current_room.update()

            # Check if the player has reached the key or the open door
            if pygame.sprite.collide_rect(player, current_room.key):
                current_room.key.rect.x = SCREEN_WIDTH
                current_room.key.rect.y = SCREEN_HEIGHT
                current_room.door.image = current_room.door.open_image
            if pygame.sprite.collide_rect(player,
                                          current_room.door) and current_room.door.image == current_room.door.open_image:
                room_done = True

            # If the player finishes the room...
            if room_done:
                # ...and there are rooms left, set up the next room.
                if current_room_no < len(room_list) - 1:
                    player.rect.x = 100
                    player.rect.y = SCREEN_HEIGHT - player.rect.height - 50
                    current_room_no += 1
                    current_room = room_list[current_room_no]
                    player.room = current_room
                    room_done = False
                # Otherwise, return to the menu.
                else:
                    level_done = True
                    player.restore()


            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_room.draw(screen)
            active_sprite_list.draw(screen)
            pellet_list.draw(screen)
            for enemy in current_room.enemy_list:
                for pellet in enemy.pellet_list:
                    shouldDel = pellet.move(current_room.tile_list, player, "e")
                    if shouldDel:
                        del pellet
                enemy.pellet_list.draw(screen)

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        # Restore the room so enemies come back if the level is replayed
        current_room.restore()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()




if __name__ == "__main__":
    main()
