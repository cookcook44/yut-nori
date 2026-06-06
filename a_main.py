from threading import Thread
import pygame
import copy
import random
import sys
# pygame.init()
pygame.font.init()

screen_size = (1200,600)
screen = pygame.display.set_mode((1200,600))
clock = pygame.time.Clock()
RED = (254, 99, 99)
BLUE = (99, 125, 254)

from link import _link
from utils import _utils
import shape
import image
import mouse

_shape = shape.Shape()
_image = image.Image()
_mouse = mouse.Mouse()

while True:
    screen.fill((186, 232, 233))
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()
            exit()
    key_pressed = pygame.key.get_pressed()
    
    #print(_link.first_link)
    if _link.first_link == 0:
        _link.account()

    _shape.board()
    _image.always()
    _shape.yut()
    _shape.mal()
    _mouse.click()

    pygame.display.flip()

    clock.tick(90)
    _utils.cnt += 1