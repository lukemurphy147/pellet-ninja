import pytest
import pygame
import sys
from player import Player

# needed to make pygame play nice with pytest
pygame.init()
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

# dummy values for player class
_player = Player(20, 20, 50, 50)

# test cases
def test_location_horizontal():
    assert _player.get_location_horizontal() == 50


def test_location_vertical():
    assert _player.get_location_vertical() == 50


def test_width():
    assert _player.get_width() == 20


def test_height():
    assert _player.get_height() == 20


def test_left():
    # this would simulate holding down the left key
    _player.move_left()
    _player.move_stop()
    assert _player.get_location_horizontal() < 50


def test_right():
    # this would simulate holding down the left key
    _player.move_right()
    _player.move_stop()
    assert _player.get_location_horizontal() == 50


def test_speed():
    # this checks that the movement value is equal to the speed value
    move = True
    while move == True:
        _player.move_right()
        assert _player.get_movement() == _player.speed
        move = False
    _player.move_stop()


def test_new_location():
    # to make sure test_speed actually moved the character
    assert _player.get_location_horizontal() > 50
