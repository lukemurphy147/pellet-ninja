import pygame
import os

"""
Module documentation
A player class module for use in Pellet Ninja. Handles a sprite, horizontal movement, spawning.
"""


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, location_x, location_y):
        """
        Player creates a new player object.
        :param width: width of sprite
        :param height: height of sprite
        :param location_x: spawn x position
        :param location_y: spawn y postion
        :return: returns nothing
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        # movement values for x, y
        self.movement = [0, 0]
        # speed of the player and eventual player's jump gravity
        self.speed = 4
        self.vertical_momentum = 0
        # list of sprites
        self.images = []
        # loading the sprite list, only one image for now
        img = pygame.image.load(os.path.join("images", "hero1.png")).convert()
        self.images.append(img)
        self.image = self.images[0]
        # values for the rect that handles the actual collision
        self.rect = self.image.get_rect()
        self.rect.x = location_x
        self.rect.y = location_y

    def get_width(self):
        """
        gets the width of the player
        :return: width
        """
        return self.width

    def get_height(self):
        """
        gets the width of the player
        :return: height
        """
        return self.height

    def move_right(self):
        """
        moves the player to the right
        """
        self.movement[0] += self.speed
        self.update()

    def move_left(self):
        """
        moves the player to the left
        """
        self.movement[0] -= self.speed
        self.update()

    def move_stop(self):
        """
        restores the player's horizontal movement to 0
        """
        self.movement[0] = 0
        self.update()

    def update(self):
        """
        updates the player's rect position
        """
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

    def get_location_horizontal(self):
        """
        finds the current location
        """
        return self.rect.x

    def get_location_vertical(self):
        """
        finds the current location
        """
        return self.rect.y

    def get_movement(self):
        """
        finds the movement value horizontal
        """
        return self.movement[0]
