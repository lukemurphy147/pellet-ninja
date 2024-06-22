import pygame

class Pellet(pygame.sprite.Sprite):

    """In game projectile"""

    def __init__(self, x: int, y: int, direction: int, fileString: str):

        """
        :param x: x position of the pellet:
        :param y: y position of the pellet
        :param direction: direction the pellet is facing:
        """
        super().__init__()

        # setting parameters utilizing Pygame sprite methods

        # direction holds a value 1 or -1, determines the directing that the pellet is moving
        self.direction = direction

        # Loading a sprite for the pellet moving right
        self.right_image = pygame.image.load("images/"+fileString+".png").convert_alpha()

        # setting it's size -> x,y
        self.right_image = pygame.transform.scale(self.right_image, (45, 35))

        # loading a sprite for the pellet moving left
        self.left_image = pygame.image.load("images/"+fileString+".png").convert_alpha()

        # setting it's size -> x, y
        self.left_image = pygame.transform.scale(self.left_image, (45, 35))

        # if direction is a positive number set the pellet to face right, else set to move left
        if direction == 1:
            self.image = self.right_image
        else:
            self.image = self.left_image

        # rectangle class uses the size given to the scale of the image, This will allow for easy hit detection
        self.rect = self.image.get_rect()

        # setting the x, y coordinates of the pellet
        self.rect.x = x
        self.rect.y = y



    def move(self, others, enemies, pelletShooter):
        """Moves 20 pixels to the left or right"""

        # If the pellet collides with something, the pellet should be killed, or deleted
        kill = True

        # If the pellet was shot by the player
        if pelletShooter == "p":

            # check to see if the pellet collides with any enemies
            for enemy in enemies:

                # if the pellet collides with an enemy, make the enemy take damage
                if pygame.sprite.spritecollideany(self,[enemy]):
                    pygame.sprite.Sprite.kill(self)

                    # if the enemies health is now 0, kill it and delete it
                    if enemy.take_damage() <= 0:
                        pygame.sprite.Sprite.kill(enemy)
                        del enemy

        # If the pellet was shot by an enemy
        elif pelletShooter == "e":

            # Check to see if the pellet collides with the player, if it does, damage the player
            if pygame.sprite.spritecollideany(self,[enemies]):
                pygame.sprite.Sprite.kill(self)
                enemies.take_damage()

        # Check to see if the pellet collides with any tiles
        if pygame.sprite.spritecollideany(self, others):
            pygame.sprite.Sprite.kill(self)

        # If the pellet collides with nothing, move it. Kill is now false, meaning do not delete the pellet
        else:
            self.rect.x += 20 * self.direction
            kill = False

        return kill