from threading import Thread
import pygame
import random
import copy
import sys
pygame.init()
screen_size = (1200,600)
screen = pygame.display.set_mode((1200,600))

from link import sock
from link import _link
from utils import _utils
import image

# _utils = utils.Utils()  # 0
_image = image.Image()

class Shape:
    def __init__(self):
        self.wanna_move = -1
    def board(self):
        pygame.draw.rect(screen, (154, 230, 153), (0,0,600,600)) #왼쪽보드
        if _utils.selected == 2: # 오른쪽보드
            pygame.draw.rect(screen, (255, 223, 122), (650, 175, 500, 250))
        else:
            pygame.draw.rect(screen, (255, 245, 161), (650, 175, 500, 250))
        if _utils.verified == 1:
            for i in range(4):
                pygame.draw.circle(screen, (254, 199, 127), (156+i*96, 60), 20) # 위쪽
                pygame.draw.circle(screen, (254, 199, 127), (156+i*96, 540), 20) # 아래쪽
                pygame.draw.circle(screen, (254, 199, 127), (60, 156+i*96), 20) # 왼쪽
                pygame.draw.circle(screen, (254, 199, 127), (540, 156+i*96), 20) # 오른쪽
            for i in range(5):
                pygame.draw.circle(screen, (254, 199, 127), (140+i*80, 140+i*80), 20)
                pygame.draw.circle(screen, (254, 199, 127), (140+i*80, 460-i*80), 20)
            pygame.draw.circle(screen, (248, 176, 85), (60, 60), 30)
            pygame.draw.circle(screen, (248, 176, 85), (540, 60), 30)
            pygame.draw.circle(screen, (248, 176, 85), (60, 540), 30)
            pygame.draw.circle(screen, (248, 176, 85), (540, 540), 30)
            pygame.draw.circle(screen, (248, 176, 85), (300, 300), 30)

            if not hasattr(_utils, 'turnchange'):
                def get_turn():
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            sent_msg = data.decode('utf-8')
                            if sent_msg == 'change':
                                if _utils.turn == 'R':
                                    _utils.turn = 'B'
                                elif _utils.turn == 'B':
                                    _utils.turn = 'R'
                            else:
                                print('else') # 프린트되면 오류임
                        except:
                            pass
                
                thread5 = Thread(target=get_turn, daemon=True)
                thread5.start()
                _utils.turnchange = True

        elif _utils.verified == 0:
            pygame.draw.rect(screen, (255, 245, 161), (100, 130, 400, 150))
            pygame.draw.rect(screen, (255, 245, 161), (100, 320, 400, 150))
            _utils.draw_text_center(text="당신", center=(142, 158), font_size=30)
            _utils.draw_text_center(text="상대", center=(142, 348), font_size=30)
            if _utils.prematch[_utils.user-1] == 2:
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((325, 205), (40, 105)))
            elif _utils.prematch[_utils.user-1] == 1:
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((325, 205), (40, 105)))
            elif _utils.prematch[_utils.user-1] == 0:
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((325, 205), (40, 105)))
            elif _utils.prematch[_utils.user-1] == 0:
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((325, 205), (40, 105)))
            
            if not hasattr(_utils, 'dataget'):
                def get_data():
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            sent_msg = data.decode('utf-8')
                            if sent_msg == '0':
                                _utils.prematch[abs(_utils.user-2)] = 2
                            elif sent_msg == '1':
                                _utils.prematch[abs(_utils.user-2)] = 1
                            else:
                                _utils.prematch[abs(_utils.user-2)] = 0
                        except:
                            pass
                
                thread3 = Thread(target=get_data, daemon=True)
                thread3.start()
                _utils.dataget = True
            #print(_utils.user) # 만일 0이면, link.py가 먼저 되고 utils의 __init__이 되는 것
            if _utils.prematch[abs(_utils.user-2)] == 2:
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((325, 395), (40, 105)))
            elif _utils.prematch[abs(_utils.user-2)] == 1:
                screen.blit(_image.yut_back_small, _utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((325, 395), (40, 105)))
            elif _utils.prematch[abs(_utils.user-2)] == 0:
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(_image.yut_front_small, _utils.center_to_lefttop((325, 395), (40, 105)))
            
            # 다르면 결과, 안 다르면 다시 하기
            if _utils.prematch[_utils.user-1] != -1 and _utils.prematch[abs(_utils.user-2)] != -1:
                if _utils.prematch[_utils.user-1] == _utils.prematch[abs(_utils.user-2)]:
                    _utils.roll += 1
                    _utils.rollable += 1
                    _utils.prematch = [-1, -1] # 비기면 3개 초기화
                else:
                    if _utils.prematch[0] > _utils.prematch[1]:
                        if _utils.user == 1:
                            _utils.who = 'R' # red가 선
                        else:
                            _utils.who = 'B'
                    else:
                        if _utils.user == 1:
                            _utils.who = 'B' # red가 선
                        else:
                            _utils.who = 'R'
                    if _utils.who == 'R':
                        saverfd = '빨강 (선공)'
                    else:
                        saverfd = '파랑 (후공)'
                    _utils.draw_text_center(text=f"당신: {saverfd}", center=(300, 280), color=(0,0,0), font_size = 40)
                    if _utils.cnt > 250:
                        _utils.cnt = 0
                    if _utils.cnt > 240:
                        _utils.rollable = 1
                        #_utils.roll = -1 
                        _utils.verified = 1
                


    def yut(self):
        if _utils.rollable > 0 and _utils.verified == 1:
            _utils.draw_text_center(text=f"{_utils.rollable}", center=(1170, 70), font_size=35)
        if _utils.who == 'R':
            pygame.draw.circle(screen, (254, 99, 99), (1170, 35), 17)
        elif _utils.who == 'B': 
            pygame.draw.circle(screen, (99, 125, 254), (1170, 35), 17)
        if _utils.selected == 2 and _utils.rollable > 0:
            if _utils.verified != 1 or _utils.who == _utils.turn:
                pygame.draw.rect(screen, (215, 255, 128), (800, 260, 200, 80))
                _utils.draw_text_center(text="굴리기", center=(900, 300), font_size=40)
        
        if _utils.verified == 1:
            if _utils.selected == 3:
                pygame.draw.rect(screen, (255, 223, 122), (650, 450, 80, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (650, 450, 80, 125))

            _utils.draw_text_center(text="차례", center=(690, 480), font_size=25)
            if _utils.turn == 'R':
                pygame.draw.circle(screen, (254, 99, 99), (690, 535), 25)
            elif _utils.turn == 'B':
                pygame.draw.circle(screen, (99, 125, 254), (690, 535), 25)
        
            if _utils.selected == 4:
                pygame.draw.rect(screen, (255, 223, 122), (755, 450, 185, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (755, 450, 185, 125))
            if _utils.selected == 5:
                pygame.draw.rect(screen, (255, 223, 122), (965, 450, 185, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (965, 450, 185, 125))
            if len(_utils.usable) >= 1:
                for i in range(len(_utils.usable)):
                    if self.wanna_move == i+1:
                        pygame.draw.rect(screen, (216, 255, 161), (650+i*105, 25, 80, 125))
                    else:
                        pygame.draw.rect(screen, (255, 245, 161), (650+i*105, 25, 80, 125))
                    _utils.draw_text_center(text=f"{_utils.number_to_yut(_utils.usable[i])[0]}", center=(690+i*105,82.5), font_size=30)

    def mal(self):
        if _utils.verified == 1:
            if _utils.left[0] >= 1:
                for i in range(_utils.left[0]):
                    pygame.draw.circle(screen, (254, 99, 99), (847.5-(_utils.left[0]-1)*25 + i*50, 512.5), 22)
            if _utils.left[1] >= 1:
                for i in range(_utils.left[1]):
                    pygame.draw.circle(screen, (99, 125, 254), (1057.5-(_utils.left[1]-1)*25 + i*50, 512.5), 22)

            if self.wanna_move != -1: # 판에 놓는 위치 그거. 움직일 족보를 선택하고,
                if (_utils.selected == 4 and _utils.turn == 'R') or (_utils.selected == 5 and _utils.turn == 'B'): # 움직일 말을 선택하면,
                    if (_utils.turn == 'R' and _utils.left[0] >= 1) or (_utils.turn == 'B' and _utils.left[1] >= 1):
                        pygame.draw.circle(screen, (88, 48, 44), _utils.number_to_loc(_utils.number_to_yut(_utils.usable[self.wanna_move-1])[2]), 15) # 족보,말 선택하면 판에 띄워줌

            if _utils.selected == 6:
                pygame.draw.circle(screen, (88, 48, 44), _utils.number_to_loc(_utils.where_to_go(_utils.mal, _utils.number_to_yut(_utils.usable[self.wanna_move-1])[2], _utils.turn)), 15)

            for i in range(32): # _utils.board를 판에 구현
                if _utils.board[i][0] != '_': 
                    if _utils.board[i][0] == 'R':
                        color = (254, 99, 99)
                    elif _utils.board[i][0] == 'B':
                        color = (99, 125, 254)
                    pygame.draw.circle(screen, color, _utils.number_to_loc(i), 13)
                    if _utils.board[i][1] > 1:
                        _utils.draw_text_center(text=f"{_utils.board[i][1]}", center=(_utils.number_to_loc(i)[0], _utils.number_to_loc(i)[1]-3), color=(255,255,255), font_size=20)

            if _utils.selected == 6 and _utils.mal != 30 and _utils.mal != 31:
                _utils.draw_text_center(text="v", center=(_utils.number_to_loc(_utils.mal)[0], _utils.number_to_loc(_utils.mal)[1]-3), color=(0,0,0), font_size=19)

            if _utils.gameover != '_':
                _utils.selected = -1
                if _utils.gameover == 'R':
                    winner = 'Red'
                else:
                    winner = 'Blue'
                _utils.draw_text_center(text=f"{winner} Win!", center=(300, 240), color=(0,0,0), font_size = 100)
            
            if _utils.turnover > 0:
                _utils.turnover -= 1
                _utils.draw_text_center(text=f"빽도를 쓸 수 없어서 턴 넘어감", center=(300, 280), color=(0,0,0), font_size = 40)

            #if _utils.who == 'R':
            #    pygame.draw.circle(screen, RED, (1190, 10), 10)
            #elif _utils.who == 'B':
            #     pygame.draw.circle(screen, BLUE, (1190, 10), 10)