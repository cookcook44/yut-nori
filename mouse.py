from threading import Thread
import pygame
import random
import copy
import sys
pygame.init()
screen_size = (1200,600)
screen = pygame.display.set_mode((1200,600))


import shape
from link import sock
from link import _link
from utils import _utils

_shape = shape.Shape()

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    def check(self, tl, wh, x,y): # top left, width height x y 입력하면 사각형 안에 x y가 있는지 체크해줌
        if tl[0] < x < tl[0] + wh[0] and tl[1] < y < tl[1] + wh[1]:
            return True
        else:
            return False

    def click(self):
        if (pygame.mouse.get_pressed (num_buttons = 3)[0] == True) and _utils.gameover == '_':
            self.x = pygame.mouse.get_pos ( )[0]
            self.y = pygame.mouse.get_pos ( )[1]
            if _utils.verified == 0:
                if _utils.selected == 2 and _utils.rollable > 0 and self.check((800, 260), (200, 80), self.x, self.y) and _utils.cnt>20:
                    _utils.roll = 1
                    _utils.selected = -1
                    _utils.cnt = 0
                elif self.check((650, 175), (500, 250), self.x, self.y) and _utils.cnt>20 and (_utils.verified != 1 or _utils.who == _utils.turn):
                    _utils.selected = 2
                    _utils.cnt = 0

            elif _utils.verified == 1:
                if _utils.selected == 2 and _utils.rollable > 0 and self.check((800, 260), (200, 80), self.x, self.y) and _utils.cnt>20:
                    _utils.roll = 1
                    _utils.selected = -1
                    _utils.cnt = 0
                elif self.check((650, 175), (500, 250), self.x, self.y) and _utils.cnt>20 and (_utils.verified != 1 or _utils.who == _utils.turn):
                    _utils.selected = 2
                    _utils.cnt = 0
                if self.check((650, 450), (80, 125), self.x, self.y) and (_utils.verified != 1 or _utils.who == _utils.turn):
                    _utils.selected = 3
                if self.check((755, 450), (185, 125), self.x, self.y) and (_utils.verified != 1 or _utils.who == _utils.turn):
                    _utils.selected = 4
                if self.check((965, 450), (185, 125), self.x, self.y) and (_utils.verified != 1 or _utils.who == _utils.turn):
                    _utils.selected = 5
                for i in range(len(_utils.usable)):
                    if self.check((650+i*105, 25), (80, 125), self.x, self.y) and (_utils.verified != 1 or _utils.who == _utils.turn):
                        _shape.wanna_move = i+1 # 움직일 족보 선택함
                if _shape.wanna_move != -1 and ((_utils.selected == 4 and _utils.turn == 'R') or (_utils.selected == 5 and _utils.turn == 'B')) and _utils.loc_to_number(self.x, self.y, _utils.turn) == _utils.number_to_yut(_utils.usable[_shape.wanna_move-1])[2] and _utils.loc_to_number(self.x, self.y, _utils.turn) != -1: # 누른 곳이 갈 수 있는 칸과 같으면 
                    if (_utils.turn == 'R' and _utils.left[0] >= 1) or (_utils.turn == 'B' and _utils.left[1] >= 1):
                        boardloc = _utils.loc_to_number(self.x, self.y, _utils.turn)
                        if boardloc != -1: # 처음에 놓는 것
                            if _utils.turn == 'R':
                                _utils.left[0] -= 1
                                if _utils.board[boardloc][0] == '_':
                                    _utils.board[boardloc] = ['R',1]
                                elif _utils.board[boardloc][0] == 'B':
                                    _utils.left[1] += _utils.board[boardloc][1]
                                    _utils.board[boardloc] = ['R',1]
                                    if _utils.usable[_shape.wanna_move-1] != 0 and _utils.usable[_shape.wanna_move-1] != 4:
                                        _utils.rollable += 1
                                else:
                                    _utils.board[boardloc][1] += 1

                            elif _utils.turn == 'B':
                                _utils.left[1] -= 1
                                if _utils.board[boardloc][0] == '_':
                                    _utils.board[boardloc] = ['B',1]
                                elif _utils.board[boardloc][0] == 'R':
                                    _utils.left[0] += _utils.board[boardloc][1]
                                    _utils.board[boardloc] = ['B',1]
                                    if _utils.usable[_shape.wanna_move-1] != 0 and _utils.usable[_shape.wanna_move-1] != 4:
                                        _utils.rollable += 1
                                else:
                                    _utils.board[boardloc][1] += 1

                            del _utils.usable[_shape.wanna_move-1]
                            _shape.wanna_move = -1

                            if _utils.board[30][1] == 3:
                                _utils.gameover = 'R'
                            elif _utils.board[31][1] == 3:
                                _utils.gameover = 'B'
                            
                            def send_move():
                                for _ in range(10):
                                    msg = str(f"f0{boardloc}{_utils.turn}").encode("utf-8") # m/f (f는 first, m는 move), 첫 위치, 이동한 위치, 색 총 4자리 
                                    sock.sendto(msg, _link.opp_addr)
                                    pygame.time.delay(20)
                            thread6 = Thread(target=send_move)
                            thread6.start()

                            if len(_utils.usable) == 0 and _utils.rollable == 0:
                                _utils.turn_change()
                            
                        
                elif _shape.wanna_move != -1:
                    boardloc = _utils.loc_to_number(self.x, self.y, _utils.turn) # boardloc는 현재 마우스 위치 -> 보드에서의 숫자
                    if (_utils.selected != 6 or boardloc != (_utils.where_to_go(_utils.mal,_utils.number_to_yut(_utils.usable[_shape.wanna_move-1])[2], _utils.turn))) and boardloc != -1 and _utils.board[boardloc][0] == _utils.turn and boardloc != 30 and boardloc != 31 and (_utils.verified != 1 or _utils.who == _utils.turn): # 자기 기물을 누름
                        _utils.selected = 6
                        _utils.mal = boardloc # 처음에 자기 기물 누를 때 _utils.mal에 boardloc를 저장해놓음 
                    elif _utils.selected == 6 and boardloc == (_utils.where_to_go(_utils.mal,_utils.number_to_yut(_utils.usable[_shape.wanna_move-1])[2], _utils.turn)): # 자기 기물을 누른 상태에서 족보 고르고 갈 곳 누름
                        saver = _utils.board[_utils.mal]
                        _utils.board[_utils.mal] = ['_', 0] # 움직이기 전 위치 비우기
                        _utils.selected = -1
                        if _utils.turn == 'R':
                            if _utils.board[boardloc][0] == '_':
                                _utils.board[boardloc] = ['R',saver[1]] # saver[1]로 저장해놨던 말 개수를 가져옴
                            elif _utils.board[boardloc][0] == 'B':
                                _utils.left[1] += _utils.board[boardloc][1]
                                _utils.board[boardloc] = ['R',saver[1]]
                                if _utils.usable[_shape.wanna_move-1] != 0 and _utils.usable[_shape.wanna_move-1] != 4: # 모,윷으로 잡는건 +1 안됨
                                    _utils.rollable += 1
                            else:
                                _utils.board[boardloc][1] += saver[1]

                        elif _utils.turn == 'B':
                            if _utils.board[boardloc][0] == '_':
                                _utils.board[boardloc] = ['B',saver[1]]
                            elif _utils.board[boardloc][0] == 'R':
                                _utils.left[0] += _utils.board[boardloc][1]
                                _utils.board[boardloc] = ['B',saver[1]]
                                if _utils.usable[_shape.wanna_move-1] != 0 and _utils.usable[_shape.wanna_move-1] != 4: # 모,윷으로 잡는건 +1 안됨
                                    _utils.rollable += 1
                            else:
                                _utils.board[boardloc][1] += saver[1]

                        del _utils.usable[_shape.wanna_move-1]
                        _shape.wanna_move = -1

                        if _utils.board[30][1] == 3:
                            _utils.gameover = 'R'
                        elif _utils.board[31][1] == 3:
                            _utils.gameover = 'B'

                        if len(_utils.usable) == 0 and _utils.rollable == 0:
                            _utils.turn_change()