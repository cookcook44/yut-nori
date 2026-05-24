from threading import Thread
import pygame
import random
import copy
import sys
pygame.init()
screen_size = (1200,600)
screen = pygame.display.set_mode((1200,600))
from socket import socket, AF_INET, SOCK_DGRAM
sock = socket(AF_INET, SOCK_DGRAM)

import link
# import utils
# _utils = utils.Utils()
from utils import _utils
_link = link.Link()


class Image:
    def __init__(self):
        self.yut_back = pygame.image.load("z_img/yut_back.png")
        self.yut_back = pygame.transform.scale(self.yut_back, (80, 210))
        self.yut_front = pygame.image.load("z_img/yut_front.png")
        self.yut_front = pygame.transform.scale(self.yut_front, (80, 210))
        self.yut_special = pygame.image.load("z_img/yut_special.png")
        self.yut_special = pygame.transform.scale(self.yut_special, (80, 210))
        self.yut = [0,0,0,0]
        self.yut_back_small = pygame.transform.scale(self.yut_back, (40, 105))
        self.yut_front_small = pygame.transform.scale(self.yut_front, (40, 105))
    def always(self):
        if _utils.roll == -1:
            if _utils.verified == 0:
                for i in range(2):
                    if self.yut[i] == 0:
                        screen.blit(self.yut_back, _utils.center_to_lefttop((850 + 100*i, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_front, _utils.center_to_lefttop((850 + 100*i, 300), (80, 210)))
            elif _utils.verified == 1:
                for i in range(3):
                    if self.yut[i] == 0:
                        screen.blit(self.yut_back, _utils.center_to_lefttop((750 + 100*i, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_front, _utils.center_to_lefttop((750 + 100*i, 300), (80, 210)))
                    if self.yut[3] == 0:
                        screen.blit(self.yut_back, _utils.center_to_lefttop((750 + 300, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_special, _utils.center_to_lefttop((750 + 300, 300), (80, 210)))
        elif _utils.roll == 1:
            if _utils.verified == 0:
                saver = 0
                for i in range(2):
                    self.yut[i] = random.randint(0,1)
                    if self.yut[i] == 1:
                        saver += 1
                def send_saver():
                    for _ in range(10):
                        msg = str(saver).encode("utf-8")
                        sock.sendto(msg, _link.opp_addr)
                        pygame.time.delay(20)
                thread1 = Thread(target=send_saver)
                thread1.start()
                if saver == 0:
                    _utils.prematch[_utils.user-1] = 2
                elif saver == 1:
                    _utils.prematch[_utils.user-1] = 1
                else:
                    _utils.prematch[_utils.user-1] = 0
                _utils.roll = -1
                _utils.rollable -= 1

            elif _utils.verified == 1:
                saver = 0
                for i in range(3):
                    self.yut[i] = random.randint(0,1)
                    if self.yut[i] == 1:
                        saver += 1

                if saver == 0:
                    self.yut[3] = random.randint(0,1)
                    saver -= self.yut[3]
                elif saver != 0:
                    self.yut[3] = random.randint(0,1)
                    saver += self.yut[3]
                # k = random.randint(0,1)
                # if k == 0:
                #     saver = -1
                # elif k == 1:
                #     saver = 1

                _utils.usable.append(saver)
                _utils.roll = -1
                if _utils.number_to_yut(saver)[1] == 0:
                    _utils.rollable -= 1
                _utils.selected = -1
        if len(_utils.usable) == 1 and _utils.verified == 1:
            if _utils.usable[0] == -1:
                if _utils.turn == 'R' and (_utils.board[30][1] + _utils.left[0]) == 3:
                    _utils.turnover = 300
                    _utils.turn_change()
                elif _utils.turn == 'B' and (_utils.board[31][1] + _utils.left[1]) == 3:
                    _utils.turnover = 300
                    _utils.turn_change()