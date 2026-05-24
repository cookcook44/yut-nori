from threading import Thread
import pygame
import copy
import random
import sys
pygame.init()
screen_size = (1200,600)
screen = pygame.display.set_mode((1200,600))
clock = pygame.time.Clock()
cnt = 0
from socket import socket, AF_INET, SOCK_DGRAM
BUF_SIZE = 1024
sock = socket(AF_INET, SOCK_DGRAM)
RED = (254, 99, 99)
BLUE = (99, 125, 254)

import link
import shape
import image
import mouse

_link = link.Link()  # 1
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
    cnt += 1