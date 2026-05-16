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

class Utils:
    def __init__(self):
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
        utils.usable = []
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
        if utils.roll == -1:
            if utils.verified == 0:
                for i in range(2):
                    if self.yut[i] == 0:
                        screen.blit(self.yut_back, utils.center_to_lefttop((850 + 100*i, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_front, utils.center_to_lefttop((850 + 100*i, 300), (80, 210)))
            elif utils.verified == 1:
                for i in range(3):
                    if self.yut[i] == 0:
                        screen.blit(self.yut_back, utils.center_to_lefttop((750 + 100*i, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_front, utils.center_to_lefttop((750 + 100*i, 300), (80, 210)))
                    if self.yut[3] == 0:
                        screen.blit(self.yut_back, utils.center_to_lefttop((750 + 300, 300), (80, 210)))
                    else:
                        screen.blit(self.yut_special, utils.center_to_lefttop((750 + 300, 300), (80, 210)))
        elif utils.roll == 1:
            if utils.verified == 0:
                saver = 0
                for i in range(2):
                    self.yut[i] = random.randint(0,1)
                    if self.yut[i] == 1:
                        saver += 1
                def send_saver():
                    for _ in range(10):
                        msg = str(saver).encode("utf-8")
                        sock.sendto(msg, link.opp_addr)
                        pygame.time.delay(20)
                thread1 = Thread(target=send_saver)
                thread1.start()
                if saver == 0:
                    utils.prematch[utils.user-1] = 2
                elif saver == 1:
                    utils.prematch[utils.user-1] = 1
                else:
                    utils.prematch[utils.user-1] = 0
                utils.roll = -1
                utils.rollable -= 1

            elif utils.verified == 1:
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

                utils.usable.append(saver)
                utils.roll = -1
                if utils.number_to_yut(saver)[1] == 0:
                    utils.rollable -= 1
                utils.selected = -1
        if len(utils.usable) == 1 and utils.verified == 1:
            if utils.usable[0] == -1:
                if utils.turn == 'R' and (utils.board[30][1] + utils.left[0]) == 3:
                    utils.turnover = 300
                    utils.turn_change()
                elif utils.turn == 'B' and (utils.board[31][1] + utils.left[1]) == 3:
                    utils.turnover = 300
                    utils.turn_change()

class Shape:
    def __init__(self):
        self.wanna_move = -1
    def board(self):
        pygame.draw.rect(screen, (154, 230, 153), (0,0,600,600)) #왼쪽보드
        if utils.selected == 2: # 오른쪽보드
            pygame.draw.rect(screen, (255, 223, 122), (650, 175, 500, 250))
        else:
            pygame.draw.rect(screen, (255, 245, 161), (650, 175, 500, 250))
        if utils.verified == 1:
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

            if not hasattr(utils, 'turnchange'):
                def get_turn():
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            sent_msg = data.decode('utf-8')
                            if sent_msg == 'change':
                                if utils.turn == 'R':
                                    utils.turn = 'B'
                                elif utils.turn == 'B':
                                    utils.turn = 'R'
                            else:
                                print('else')
                        except:
                            pass
                
                thread5 = Thread(target=get_turn, daemon=True)
                thread5.start()
                utils.turnchange = True

        elif utils.verified == 0:
            pygame.draw.rect(screen, (255, 245, 161), (100, 130, 400, 150))
            pygame.draw.rect(screen, (255, 245, 161), (100, 320, 400, 150))
            utils.draw_text_center(text="당신", center=(142, 158), font_size=30)
            utils.draw_text_center(text="상대", center=(142, 348), font_size=30)
            if utils.prematch[utils.user-1] == 2:
                screen.blit(image.yut_back_small, utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(image.yut_back_small, utils.center_to_lefttop((325, 205), (40, 105)))
            elif utils.prematch[utils.user-1] == 1:
                screen.blit(image.yut_back_small, utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(image.yut_front_small, utils.center_to_lefttop((325, 205), (40, 105)))
            elif utils.prematch[utils.user-1] == 0:
                screen.blit(image.yut_front_small, utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(image.yut_front_small, utils.center_to_lefttop((325, 205), (40, 105)))
            elif utils.prematch[utils.user-1] == 0:
                screen.blit(image.yut_front_small, utils.center_to_lefttop((275, 205), (40, 105)))
                screen.blit(image.yut_front_small, utils.center_to_lefttop((325, 205), (40, 105)))
            
            if not hasattr(utils, 'dataget'):
                def get_data():
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            sent_msg = data.decode('utf-8')
                            if sent_msg == '0':
                                utils.prematch[abs(utils.user-2)] = 2
                            elif sent_msg == '1':
                                utils.prematch[abs(utils.user-2)] = 1
                            else:
                                utils.prematch[abs(utils.user-2)] = 0
                        except:
                            pass
                
                thread3 = Thread(target=get_data, daemon=True)
                thread3.start()
                utils.dataget = True
                
            if utils.prematch[abs(utils.user-2)] == 2:
                screen.blit(image.yut_back_small, utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(image.yut_back_small, utils.center_to_lefttop((325, 395), (40, 105)))
            elif utils.prematch[abs(utils.user-2)] == 1:
                screen.blit(image.yut_back_small, utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(image.yut_front_small, utils.center_to_lefttop((325, 395), (40, 105)))
            elif utils.prematch[abs(utils.user-2)] == 0:
                screen.blit(image.yut_front_small, utils.center_to_lefttop((275, 395), (40, 105)))
                screen.blit(image.yut_front_small, utils.center_to_lefttop((325, 395), (40, 105)))
            
            # 다르면 결과, 안 다르면 다시 하기
            if utils.prematch[utils.user-1] != -1 and utils.prematch[abs(utils.user-2)] != -1:
                if utils.prematch[utils.user-1] == utils.prematch[abs(utils.user-2)]:
                    utils.roll += 1
                    utils.rollable += 1
                    utils.prematch = [-1, -1] # 비기면 3개 초기화
                else:
                    if utils.prematch[0] > utils.prematch[1]:
                        if utils.user == 1:
                            utils.who = 'R' # red가 선
                        else:
                            utils.who = 'B'
                    else:
                        if utils.user == 1:
                            utils.who = 'B' # red가 선
                        else:
                            utils.who = 'R'
                    if utils.who == 'R':
                        saverfd = '빨강 (선공)'
                    else:
                        saverfd = '파랑 (후공)'
                    utils.draw_text_center(text=f"당신: {saverfd}", center=(300, 280), color=(0,0,0), font_size = 40)
                    global cnt
                    if cnt > 250:
                        cnt = 0
                    if cnt > 240:
                        utils.rollable = 1
                        #utils.roll = -1
                        utils.verified = 1
                


    def yut(self):
        if utils.rollable > 0 and utils.verified == 1:
            utils.draw_text_center(text=f"{utils.rollable}", center=(1170, 70), font_size=35)
        if utils.who == 'R':
            pygame.draw.circle(screen, (254, 99, 99), (1170, 35), 17)
        elif utils.who == 'B': 
            pygame.draw.circle(screen, (99, 125, 254), (1170, 35), 17)
        if utils.selected == 2 and utils.rollable > 0:
            if utils.verified != 1 or utils.who == utils.turn:
                pygame.draw.rect(screen, (215, 255, 128), (800, 260, 200, 80))
                utils.draw_text_center(text="굴리기", center=(900, 300), font_size=40)
        
        if utils.verified == 1:
            if utils.selected == 3:
                pygame.draw.rect(screen, (255, 223, 122), (650, 450, 80, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (650, 450, 80, 125))

            utils.draw_text_center(text="차례", center=(690, 480), font_size=25)
            if utils.turn == 'R':
                pygame.draw.circle(screen, (254, 99, 99), (690, 535), 25)
            elif utils.turn == 'B':
                pygame.draw.circle(screen, (99, 125, 254), (690, 535), 25)
        
            if utils.selected == 4:
                pygame.draw.rect(screen, (255, 223, 122), (755, 450, 185, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (755, 450, 185, 125))
            if utils.selected == 5:
                pygame.draw.rect(screen, (255, 223, 122), (965, 450, 185, 125))
            else:
                pygame.draw.rect(screen, (255, 245, 161), (965, 450, 185, 125))
            if len(utils.usable) >= 1:
                for i in range(len(utils.usable)):
                    if self.wanna_move == i+1:
                        pygame.draw.rect(screen, (216, 255, 161), (650+i*105, 25, 80, 125))
                    else:
                        pygame.draw.rect(screen, (255, 245, 161), (650+i*105, 25, 80, 125))
                    utils.draw_text_center(text=f"{utils.number_to_yut(utils.usable[i])[0]}", center=(690+i*105,82.5), font_size=30)

    def mal(self):
        if utils.verified == 1:
            if utils.left[0] >= 1:
                for i in range(utils.left[0]):
                    pygame.draw.circle(screen, (254, 99, 99), (847.5-(utils.left[0]-1)*25 + i*50, 512.5), 22)
            if utils.left[1] >= 1:
                for i in range(utils.left[1]):
                    pygame.draw.circle(screen, (99, 125, 254), (1057.5-(utils.left[1]-1)*25 + i*50, 512.5), 22)

            if shape.wanna_move != -1: # 판에 놓는 위치 그거. 움직일 족보를 선택하고,
                if (utils.selected == 4 and utils.turn == 'R') or (utils.selected == 5 and utils.turn == 'B'): # 움직일 말을 선택하면,
                    if (utils.turn == 'R' and utils.left[0] >= 1) or (utils.turn == 'B' and utils.left[1] >= 1):
                        pygame.draw.circle(screen, (88, 48, 44), utils.number_to_loc(utils.number_to_yut(utils.usable[self.wanna_move-1])[2]), 15) # 족보,말 선택하면 판에 띄워줌

            if utils.selected == 6:
                pygame.draw.circle(screen, (88, 48, 44), utils.number_to_loc(utils.where_to_go(utils.mal, utils.number_to_yut(utils.usable[shape.wanna_move-1])[2], utils.turn)), 15)

            for i in range(32):
                if utils.board[i][0] != '_': 
                    if utils.board[i][0] == 'R':
                        color = (254, 99, 99)
                    elif utils.board[i][0] == 'B':
                        color = (99, 125, 254)
                    pygame.draw.circle(screen, color, utils.number_to_loc(i), 13) # utils.board를 판에 구현
                    if utils.board[i][1] > 1:
                        utils.draw_text_center(text=f"{utils.board[i][1]}", center=(utils.number_to_loc(i)[0], utils.number_to_loc(i)[1]-3), color=(255,255,255), font_size=20)

            if utils.selected == 6 and utils.mal != 30 and utils.mal != 31:
                utils.draw_text_center(text="v", center=(utils.number_to_loc(utils.mal)[0], utils.number_to_loc(utils.mal)[1]-3), color=(0,0,0), font_size=19)

            if utils.gameover != '_':
                utils.selected = -1
                if utils.gameover == 'R':
                    winner = 'Red'
                else:
                    winner = 'Blue'
                utils.draw_text_center(text=f"{winner} Win!", center=(300, 240), color=(0,0,0), font_size = 100)
            
            if utils.turnover > 0:
                utils.turnover -= 1
                utils.draw_text_center(text=f"빽도를 쓸 수 없어서 턴 넘어감", center=(300, 280), color=(0,0,0), font_size = 40)

            #if utils.who == 'R':
            #    pygame.draw.circle(screen, RED, (1190, 10), 10)
            #elif utils.who == 'B':
            #     pygame.draw.circle(screen, BLUE, (1190, 10), 10)
        

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
        global cnt
        if (pygame.mouse.get_pressed (num_buttons = 3)[0] == True) and utils.gameover == '_':
            self.x = pygame.mouse.get_pos ( )[0]
            self.y = pygame.mouse.get_pos ( )[1]
            if utils.verified == 0:
                if utils.selected == 2 and utils.rollable > 0 and mouse.check((800, 260), (200, 80), self.x, self.y) and cnt>20:
                    utils.roll = 1
                    utils.selected = -1
                    cnt = 0
                elif mouse.check((650, 175), (500, 250), self.x, self.y) and cnt>20 and (utils.verified != 1 or utils.who == utils.turn):
                    utils.selected = 2
                    cnt = 0

            elif utils.verified == 1:
                if utils.selected == 2 and utils.rollable > 0 and mouse.check((800, 260), (200, 80), self.x, self.y) and cnt>20:
                    utils.roll = 1
                    utils.selected = -1
                    cnt = 0
                elif mouse.check((650, 175), (500, 250), self.x, self.y) and cnt>20 and (utils.verified != 1 or utils.who == utils.turn):
                    utils.selected = 2
                    cnt = 0
                if mouse.check((650, 450), (80, 125), self.x, self.y) and (utils.verified != 1 or utils.who == utils.turn):
                    utils.selected = 3
                if mouse.check((755, 450), (185, 125), self.x, self.y) and (utils.verified != 1 or utils.who == utils.turn):
                    utils.selected = 4
                if mouse.check((965, 450), (185, 125), self.x, self.y) and (utils.verified != 1 or utils.who == utils.turn):
                    utils.selected = 5
                for i in range(len(utils.usable)):
                    if mouse.check((650+i*105, 25), (80, 125), self.x, self.y) and (utils.verified != 1 or utils.who == utils.turn):
                        shape.wanna_move = i+1 # 움직일 족보 선택함
                if shape.wanna_move != -1 and ((utils.selected == 4 and utils.turn == 'R') or (utils.selected == 5 and utils.turn == 'B')) and utils.loc_to_number(self.x, self.y, utils.turn) == utils.number_to_yut(utils.usable[shape.wanna_move-1])[2] and utils.loc_to_number(self.x, self.y, utils.turn) != -1: # 누른 곳이 갈 수 있는 칸과 같으면 
                    if (utils.turn == 'R' and utils.left[0] >= 1) or (utils.turn == 'B' and utils.left[1] >= 1):
                        boardloc = utils.loc_to_number(self.x, self.y, utils.turn)
                        if boardloc != -1:
                            if utils.turn == 'R':
                                utils.left[0] -= 1
                                if utils.board[boardloc][0] == '_':
                                    utils.board[boardloc] = ['R',1]
                                elif utils.board[boardloc][0] == 'B':
                                    utils.left[1] += utils.board[boardloc][1]
                                    utils.board[boardloc] = ['R',1]
                                    if utils.usable[shape.wanna_move-1] != 0 and utils.usable[shape.wanna_move-1] != 4:
                                        utils.rollable += 1
                                else:
                                    utils.board[boardloc][1] += 1

                            elif utils.turn == 'B':
                                utils.left[1] -= 1
                                if utils.board[boardloc][0] == '_':
                                    utils.board[boardloc] = ['B',1]
                                elif utils.board[boardloc][0] == 'R':
                                    utils.left[0] += utils.board[boardloc][1]
                                    utils.board[boardloc] = ['B',1]
                                    if utils.usable[shape.wanna_move-1] != 0 and utils.usable[shape.wanna_move-1] != 4:
                                        utils.rollable += 1
                                else:
                                    utils.board[boardloc][1] += 1

                            del utils.usable[shape.wanna_move-1]
                            shape.wanna_move = -1

                            if utils.board[30][1] == 3:
                                utils.gameover = 'R'
                            elif utils.board[31][1] == 3:
                                utils.gameover = 'B'

                            if len(utils.usable) == 0 and utils.rollable == 0:
                                utils.turn_change()
                            
                        
                elif shape.wanna_move != -1:
                    boardloc = utils.loc_to_number(self.x, self.y, utils.turn) # boardloc는 현재 마우스 위치 -> 보드에서의 숫자
                    if (utils.selected != 6 or boardloc != (utils.where_to_go(utils.mal,utils.number_to_yut(utils.usable[shape.wanna_move-1])[2], utils.turn))) and boardloc != -1 and utils.board[boardloc][0] == utils.turn and boardloc != 30 and boardloc != 31 and (utils.verified != 1 or utils.who == utils.turn): # 자기 기물을 누름
                        utils.selected = 6
                        utils.mal = boardloc # 처음에 자기 기물 누를 때 utils.mal에 boardloc를 저장해놓음 
                    elif utils.selected == 6 and boardloc == (utils.where_to_go(utils.mal,utils.number_to_yut(utils.usable[shape.wanna_move-1])[2], utils.turn)): # 자기 기물을 누른 상태에서 족보 고르고 갈 곳 누름
                        saver = utils.board[utils.mal]
                        utils.board[utils.mal] = ['_', 0] # 움직이기 전 위치 비우기
                        utils.selected = -1
                        if utils.turn == 'R':
                            if utils.board[boardloc][0] == '_':
                                utils.board[boardloc] = ['R',saver[1]] # saver[1]로 저장해놨던 말 개수를 가져옴
                            elif utils.board[boardloc][0] == 'B':
                                utils.left[1] += utils.board[boardloc][1]
                                utils.board[boardloc] = ['R',saver[1]]
                                if utils.usable[shape.wanna_move-1] != 0 and utils.usable[shape.wanna_move-1] != 4: # 모,윷으로 잡는건 +1 안됨
                                    utils.rollable += 1
                            else:
                                utils.board[boardloc][1] += saver[1]

                        elif utils.turn == 'B':
                            if utils.board[boardloc][0] == '_':
                                utils.board[boardloc] = ['B',saver[1]]
                            elif utils.board[boardloc][0] == 'R':
                                utils.left[0] += utils.board[boardloc][1]
                                utils.board[boardloc] = ['B',saver[1]]
                                if utils.usable[shape.wanna_move-1] != 0 and utils.usable[shape.wanna_move-1] != 4: # 모,윷으로 잡는건 +1 안됨
                                    utils.rollable += 1
                            else:
                                utils.board[boardloc][1] += saver[1]

                        del utils.usable[shape.wanna_move-1]
                        shape.wanna_move = -1

                        if utils.board[30][1] == 3:
                            utils.gameover = 'R'
                        elif utils.board[31][1] == 3:
                            utils.gameover = 'B'

                        if len(utils.usable) == 0 and utils.rollable == 0:
                            utils.turn_change()
                    
class Link:
    def __init__(self):
        self.my_addr = ("_", -1)
        self.opp_addr = ("_", -1)
        self.first_link = 0
    def account(self):
        self.first_link = 1
        try:
            self.my_addr = ("127.0.0.1", 8000)
            self.opp_addr = ("127.0.0.1", 8001)
            sock.bind(self.my_addr)
            utils.user = 1
        except OSError:
            self.my_addr = ("127.0.0.1", 8001)
            self.opp_addr = ("127.0.0.1", 8000)
            sock.bind(self.my_addr)
            utils.user = 2

utils = Utils()
image = Image()
shape = Shape()
mouse = Mouse()
link = Link()

while True:
    screen.fill((186, 232, 233))
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()
            exit()
    key_pressed = pygame.key.get_pressed()
    
    if link.first_link == 0:
        link.account()

    shape.board()
    image.always()
    shape.yut()
    shape.mal()
    mouse.click()

    pygame.display.flip()

    clock.tick(90)
    cnt += 1