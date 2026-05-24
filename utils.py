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

import link as link

class Utils:
    def __init__(self):  # 생성자 함수
        self.turn = 'R' # 누구 차례인지
        self.left = [3,3]
        self.usable = []
        self.selected = -1
        self.roll = -1
        self.rollable = 1
        self.board = []
        self.mal = -1
        self.gameover = '_'
        self.turnover = 0
        self.who = '_' # 내부에서 저장된 유저 색
        self.verified = 0
        self.prematch = [-1,-1] 
        self.user = 0 # 터미널로 구분하는 유저
        self.stop = 0
        self.stoptwo = 0
        for _ in range(32):
            self.board.append(['_',0])
    def center_to_lefttop(self, center, size):
        realcent = (int(center[0]) - (int(size[0])/2), int(center[1]) - (int(size[1])/2))
        return realcent
    def draw_text_center(self, text, center=(0, 0), color=(0, 0, 0), font_size=20):
        font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect(center=center)
        screen.blit(text, text_rect)
    def turn_change(self):
        if self.turn == 'R':
            self.turn = 'B'
        elif self.turn == 'B':
            self.turn = 'R'
        self.rollable = 1
        self.usable = []
        if not hasattr(self, 'moveget'):
                def get_move():
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            sent_msg = data.decode('utf-8')
                            if sent_msg == '0':
                                self.prematch[abs(self.user-2)] = 2
                            elif sent_msg == '1':
                                self.prematch[abs(self.user-2)] = 1
                            else:
                                self.prematch[abs(self.user-2)] = 0
                        except:
                            pass
                
                thread7 = Thread(target=get_move, daemon=True)
                thread7.start()
                self.moveget = True

        def send_turn():
            for _ in range(10):
                msg = str('change').encode("utf-8")
                sock.sendto(msg, link.opp_addr)
                pygame.time.delay(20)
        thread4 = Thread(target=send_turn)
        thread4.start()
    
    def number_to_yut(self, x):
        if x == -1:
            return ['빽도', 0,-1]
        elif x == 0:
            return ['모', 1,5]
        elif x == 1:
            return ['도', 0,1]
        elif x == 2:
            return ['개', 0,2]
        elif x == 3:
            return ['걸', 0,3]
        elif x == 4:
            return ['윷', 1,4]
    def number_to_loc(self, x):
        if 0 <= x < 5:
            return (540, 156+(4-x)*96)
        elif 5 <= x < 10:
            return (156+(9-x)*96, 60)
        elif 10 <= x < 15:
            return (60, 60+(x-10)*96)
        elif 15 <= x < 20:
            return (60+(x-15)*96, 540)
        elif x == 20:
            return (300,300)
        elif 21 <= x < 23:
            return (140+(25-x)*80, 460-(25-x)*80)
        elif 23 <= x < 25:
            return (140+(x-23)*80, 140+(x-23)*80)
        elif 25 <= x < 27:
            return (140+(26-x)*80, 460-(26-x)*80)
        elif 27 <= x < 29:
            return (140+(x-24)*80, 140+(x-24)*80)
        elif x == 29:
            return (540, 540)
        elif x == 30:
            return (565, 585)
        elif x == 31:
            return (585, 565)
        else:
            return (700, 700)
    def loc_to_number(self, x, y, color):
        for i in range(5):
            if (x-540)**2 + (y-60-96*(5-i))**2 <= 225:
                if i != 0:
                    return i
                elif i == 0:
                    return 29
        for i in range(5):
            if (x-60-96*(5-i))**2 + (y-60)**2 <= 225:
                return i+5
        for i in range(5):
            if (x-60)**2 + (y-60-96*i)**2 <= 225:
                return i+10
        for i in range(5):
            if (x-60-96*i)**2 + (y-540)**2 <= 225:
                return i+15
        if (x-300)**2 + (y-300)**2 <= 225:
            return 20
        for i in range(2):
            if (x-460+80*i)**2 + (y-140-80*i)**2 <= 225:
                return i+21
        for i in range(2):
            if (x-140-80*i)**2 + (y-140-80*i)**2 <= 225:
                return i+23
        for i in range(2):
            if (x-140-80*(1-i))**2 + (y-460+80*(1-i))**2 <= 225:
                return i+25
        for i in range(2):
            if (x-460+80*(1-i))**2 + (y-460+80*(1-i))**2 <= 225:
                return i+27
        if (x-565)**2 + (y-585)**2 <= 225 and color == 'R':
            return 30
        if (x-585)**2 + (y-565)**2 <= 225 and color == 'B':
            return 31
        return -1
    def where_to_go(self, l, x, color): # 이전위치 숫자랑 얼마나 이동할지 받음
        if x == -1: # 빽도 
            if 2 <= l <= 19 or l == 22 or l == 24 or l == 26 or l == 28:
                return l-1
            if l == 1:
                return 29
            if l == 29:
                return 1
            if l == 21:
                return 5
            if l == 23:
                return 10
            if l == 25:
                return 20
            if l == 27:
                return 20
            if l == 20:
                return 22
            return l
            
        if 0 < l < 5 or 6 <= l < 10 or 11 <= l <= 15:
            return l+x
        elif l == 5:
            if 1 <= x <= 2:
                return 20 + x
            elif x == 3:
                return 20
            elif 4 <= x <= 5:
                return 21 + x
        elif l == 10:
            if 1 <= x <= 2:
                return 22 + x
            elif x == 3:
                return 20
            elif 4 <= x <= 5:
                return 23 + x
        elif l == 20:
            if 1 <= x <= 2:
                return 26 + x
            else:
                return 29
        elif 21 <= l <= 22:
            if l+x <= 22:
                return l+x
            elif l+x == 23:
                return 20
            elif 24 <= l+x <= 25:
                return l+x+1
            else:
                return l+x-11
        elif 23 <= l <= 24:
            if l+x <= 24:
                return l+x 
            elif l+x == 25:
                return 20
            elif 26 <= l+x <= 27:
                return l+x+1
            else:
                return 29
        elif 25 <= l <= 26:
            if l+x <= 26:
                return l+x
            else:
                return l+x-12
        elif 27 <= l <= 28:
            if l+x <= 28:
                return l+x
            else:
                return 29
        elif 16 <= l <= 19:
            if l+x <= 19:
                return l+x
            elif l+x >= 20:
                return 29
        elif l == 29 and color == 'R':
            return 30
        elif l == 29 and color == 'B':
            return 31
        elif l == 30 or l == 31:
            return -2

_utils = Utils()  # utils.py 모듈에서 단 한번만 인스턴스를 생성하고,
# 이것이 필요한 다른 모듈에서 _utils 변수를 import하여 사용한다.