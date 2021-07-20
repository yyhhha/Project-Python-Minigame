import pygame
from pygame.rect import *
import random
from time import sleep
import tkinter
from tkinter import *
from tkinter import messagebox
import sys
from pygame import mixer
import gettext
import math
from pygame.locals import *

screen_width = 800
screen_height = 600
shuttle_width = 110
shuttle_height = 100
asteroid_width = 80
asteroid_height = 70
d_count = 0
s_num = 3
scr = 0


userName =''
cnt =0
user=[] ## 사용자 숫자 정보를 넣기위한 리스트
com=[]

CENTER_WIDTH = 350
CENTER_HEIGHT = 200
updateTime = 0
updateIndex = 0
choiceUser, choiceCom = -1, -1
result = -1
win, lose, draw = 0, 0, 0

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600  #게임창 크기 지정

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
YELLOW = (250, 250, 20)
BLUE = (20, 20, 250)
GRAY = (150, 150, 150)
RED = (230, 0, 0)
fps_clock = pygame.time.Clock()
FPS = 60
score = 0

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
space = 0


def startGame():
    global screen, clock, shuttle, missile, asteroid, s_shot, s_explode, s_destroy, background, select_sound,\
    default_font, background_img, explosion_sound, warp_sound,\
    pImages, player1, recPlayer, rock_sound,\
    sound_racing, sound_crush, sound_engine
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    shuttle = pygame.image.load('shuttle.png')
    shuttle = pygame.transform.scale(shuttle, (shuttle_width, shuttle_height))
    asteroid = pygame.image.load('ast.png')
    asteroid = pygame.transform.scale(asteroid, (asteroid_width, asteroid_height))
    missile = pygame.image.load('mis.png')
    s_shot = pygame.mixer.Sound('shot.wav')
    s_explode = pygame.mixer.Sound('explosion.wav')
    s_destroy = pygame.mixer.Sound('small.wav')
    clock = pygame.time.Clock()
    background = pygame.image.load('back.jpg')
    select_sound = pygame.mixer.Sound('Heavenly Loop.wav')
    #########################################################
   #기초 폰트, 배경사진 선정, 폭발소리, 워프소리 삽입
    default_font = pygame.font.Font('NanumGothic.ttf', 28)
    background_img = pygame.image.load('background.jpg')
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    warp_sound = pygame.mixer.Sound('warp.wav')
    pygame.mixer.music.load('Inner_sanctum.wav')
    ##################################################################################################
    pImages = ['rock.png', 'scissors.png', 'paper.png']
    player1 = [pygame.image.load(pImages[i]) for i in range(len(pImages))]
    player1 = [pygame.transform.scale(player1[i], (100, 100)) for i in range(len(player1))]
    recPlayer = [player1[i].get_rect() for i in range(len(player1))]
    rock_sound = pygame.mixer.Sound('lassolady.ogg')
    ####################################################################################################
    sound_racing = pygame.mixer.Sound('race.wav')
    sound_crush = pygame.mixer.Sound('crash.wav')
    sound_engine = pygame.mixer.Sound('engine.wav')
    
def select():
    pygame.display.set_caption('Play Data')
    ground = pygame.image.load('heaven.jpg')
    ground = pygame.transform.scale(ground, (screen_width, screen_height))
    screen.blit(ground, (0, 0))
    pygame.display.set_icon(pygame.image.load('door.png'))
    font = pygame.font.SysFont('malgungothic', 50)
#    text1 = font.render("1. ROCK SCISSORS PAPER!!!", True, (0, 0, 0))
#    text2 = font.render("2. Crush Planets", True, (0, 0, 0))
#    text3 = font.render("3. Avoid Planetary", True, (0, 0, 0))
#    screen.blit(text1, (screen_width/2-300, screen_height/2-180))
#    screen.blit(text2, (screen_width/2-300, screen_height/2-100))
#    screen.blit(text3, (screen_width/2-300, screen_height/2-20))
    
    
def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))
    
def explode():
    pygame.display.update()
    sleep(1.5)
    runGame()
    
def showScore(count1, count2):
    global screen
    font = pygame.font.SysFont('malgungothic', 20)
    text = font.render("점수 : " + str(count1), True, (255, 255, 255))
    text1 = font.render("목숨 : " + str(count2), True, (255, 255, 255))
    screen.blit(text, (0, 0))
    screen.blit(text1, (0, 30))
    
def gameOver():
    global screen, d_count, s_num, scr, screen_width, screen_height
    flag = 0
    font = pygame.font.SysFont('malgungothic', 50)
    font1 = pygame.font.SysFont('malgungothic', 30)
    if d_count == 100:
        text = font.render("Mission Complete!", True, (0, 255, 0))
        text1 = font1.render("press R - Restart", True, (0, 255, 0))
        screen.blit(text, (screen_width/2-210, screen_height/2-100))
        screen.blit(text1, (screen_width/2-120, screen_height/2-30))
        d_count = 0
    else:
        text = font.render("Game Over!", True, (255, 0, 0))
        text1 = font1.render("press R - Restart", True, (255, 0, 0))
        screen.blit(text, (screen_width/2-140, screen_height/2-100))
        screen.blit(text1, (screen_width/2-120, screen_height/2-30))
        s_num = 3
    pygame.display.update()
    while True:
        if flag == 1:
            flag = 0
            d_count = 0
            s_num = 3
            screen_width = 800
            screen_height = 600
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    flag = 1
                    break
                elif event.key == pygame.K_ESCAPE:
                    flag = 1
                    scr = 0
                    break
            pygame.display.flip()
    runGame()
    
##########################################################################################################################
#우주선 클래스 만들기
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super(Spaceship, self).__init__()
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    #포지션 설정
    def set_pos(self, x, y):
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    #유저가 타 객체와 충돌했는지에 대해
    def collide(self, sprites):
        for sprite in sprites:
            #객체간의 rect이 겹쳤을 때 뭐랑 겹쳐졌는지 나타내 줌
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 운석 클래스 만들기
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Rock, self).__init__()
        # rocks = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rocks05.png', \
        #          'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rocks10.png')
        #많은 rock 중에 랜덤으로 골라서 이미지가 뜨게 만듦
        #
        # self.image = pygame.image.load(random.choice(rocks))  #왜 집합으로 만들어서 랜덤 초이스는 안 되는 걸까?
        self.image = pygame.image.load('rock02.png')
        #이미지 크기 = 객체의 크기
        self.rect = self.image.get_rect()
        #파라미터로 들어온 x, y 포지션을 넣어줌
        self.rect.x = xpos
        self.rect.y = ypos
        #수평, 수직 스피드 넣어주기
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    #돌의 방향 바꿔주기
    def set_direction(self):
        #현재 돌모양은 밑으로 내려가면 제일 예쁜 모양이라 모양을 틀어줄 것임.
        if self.hspeed > 0:
            #오른쪽으로 움직이면 270도 틀어주기
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            #왼쪽으로 움직이면 90도 틀어주기
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            #위로 움직이면 180도 틀어주기
            self.image = pygame.transform.rotate(self.image, 180)

    #암석의 속도가 바뀐다면 어떻게 할 것인가
    def update(self):
        #속도에 따라 이동하는데, 이때마다 업데이트 함수를 갱신해주는 것.
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        #만약 충돌이 발생하면 암석을 없앤다.
        if self.collide():
            self.kill()

    #충돌했을 때
    def collide(self):
        if self.rect.x < 0 < -self.rect.height or self.rect.x>WINDOW_WIDTH:
            return True
        elif self.rect.y < 0 < -self.rect.height or self.rect.y>WINDOW_HEIGHT:
            return True

#운석이 랜덤하게 나간다. 4가지 디렉션을 만들것이다.
def random_rock(speed):
    random_direction = random.randint(1, 4)
    #위에서 아래로 내려오는 암석클래스, x는 전체 랜덤값, y = 0
    if random_direction == 1:
        return Rock(random.randint(0, WINDOW_WIDTH), 0, 0, speed)
    #오른쪽에서 왼쪽으로 가는 암석 클래스
    elif random_direction == 2:
        return Rock(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT), -speed, 0)
    #아래에서 위로 올라가는 암석클래스
    elif random_direction == 3:
        return Rock(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT, 0, -speed)
    #왼쪽에서 오른쪽으로 가는 암석 클래스
    elif random_direction == 4:
        return Rock(0, random.randint(0, WINDOW_HEIGHT), speed, 0)

#워프 아이템 만들기
class Warp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Warp, self).__init__()
        self.image = pygame.image.load('warp.png')
        self.rect = self.image.get_rect()
        #x, y를 유지해서 등장할 때 마다 우주선이 가서 아이템을 먹을 수 있음.
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery

#배경이미지 repeating 백그라운드 이미지를 반복해서 배경 이미지로 만들고 싶어서.
def draw_repeating_background(background_img):
    background_rect = background_img.get_rect()
    for i in range(int(math.ceil(WINDOW_WIDTH / background_rect.width))):
        for j in range(int(math.ceil(WINDOW_HEIGHT / background_rect.height))):
            #rect을 정의하고, 정의한 크기만금 백그라운드 이미지로 반복해서 배경을 사용할 것임.
            screen.blit(background_img, Rect(i * background_rect.width,
                                             j * background_rect.height,
                                             background_rect.width,
                                             background_rect.height))

#텍스트 함수 정의
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    #폰트 크기
    text_rect = text_obj.get_rect()
    #위치 지정
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def game_loop():
    global score
    #내 마우스 포인트를 보이지 않게 한다.
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)
    spaceship = Spaceship()
    # '*' 이 기호는 여러개가 올 수 있는 기능
    spaceship.set_pos(*pygame.mouse.get_pos())
    rocks = pygame.sprite.Group()
    warps = pygame.sprite.Group()

    #최대, 최소 속도, 발생되는 운석 수
    min_rock_speed = 1
    max_rock_speed = 1
    occur_of_rocks = 1
    #발생 확률
    occur_prob = 13
    score = 0
    warp_count = 1
    #실시간성을 띄게 만들고, 쉬고 싶다면 p를 누르면 쉴 수 있있 구현할 것임.
    paused = False
    flag = 0

    while True:
        pygame.display.update()
        fps_clock.tick(FPS)

        if paused: #만약에 멈췄을 경우
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #만약 키가 눌렸는데 p값이면 다시 시작하고, 마우스포인트도 다시 감추어준다.
                    if event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_visible(False)
                #quit하면 게임이 끝난다.
                if event.type == QUIT:
                    return 'quit'
        else:
            if flag == 1:
                flag = 0
                break
            #백그라운드 이미지를 그려줌.
            draw_repeating_background(background_img)
            #난이도에 관련되게 생성
            occur_of_rocks = 1 + int(score / 500)
            min_rock_speed = 1 + int(score / 400)
            max_rock_speed = 1 + int(score / 300)

            #난이도가 얼마나 빈번하게 나타낼 것인지. occur_prob가 15인데
            #1~15사이에서 1이 나올 확률 = 1/15
            if random.randint(1, occur_prob) == 1:
                #운석이 1개 더해지면 점수도 1점 더해짐
                for i in range(occur_of_rocks):
                    rocks.add(random_rock(random.randint(min_rock_speed, max_rock_speed)))
                    score += 1

                #워프는 레어하게 나오게 하고 싶어서 1/150으로 함
                if random.randint(1, occur_prob * 10) == 1:
                    warp = Warp(random.randint(30, WINDOW_WIDTH - 30),
                                random.randint(30, WINDOW_HEIGHT - 30))
                    warps.add(warp)

            draw_text('SCORE: {}'.format(score), default_font, screen, 80, 20, YELLOW)
            draw_text('WARP: {}'.format(warp_count), default_font, screen, 700, 20, BLUE)
            rocks.update()
            warps.update()
            rocks.draw(screen)
            warps.draw(screen)

            #워프에 닿으면 죽으면 안 되고 아이템을 획득해야한다.
            warp = spaceship.collide(warps)
            if spaceship.collide(rocks):
                explosion_sound.play()
                pygame.mixer.music.stop()
                rocks.empty()
                return 'game_screen'
            elif warp: # 워프의 갯수만 증가, 아이템은 삭제
                warp_count += 1
                warp.kill()

            screen.blit(spaceship.image, spaceship.rect)

            for event in pygame.event.get():
                #키보드가 아닌 마우스로 커서를 움직일 것이다.
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    #화면 밖으로 튀어나가면 반대쪽으로 나오게 할 것임.
                    #X좌표가 10보다 작을 때, 반대편에서 화살표가 튀어나오고, Y값은 고정
                    if mouse_pos[0] <= 10:
                        pygame.mouse.set_pos(WINDOW_WIDTH - 10, mouse_pos[1])
                    elif mouse_pos[0] >= WINDOW_WIDTH -10:
                        pygame.mouse.set_pos(10, mouse_pos[1]) ####0 + 10
                    # Y좌표가 10보다 작을 때, 반대편에서 화살표가 튀어나오고, X값은 고정
                    elif mouse_pos[1] <= 10:
                        pygame.mouse.set_pos(mouse_pos[0], WINDOW_HEIGHT - 10)
                    elif mouse_pos[1] >= WINDOW_HEIGHT - 10:
                        pygame.mouse.set_pos(mouse_pos[0], 10) ####0+10
                        #마우스에 따라 우주선이 움직이니까, 마우스에 set pos를 입력
                    spaceship.set_pos(*mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if warp_count > 0:
                        warp_count -= 1
                        warp_sound.play()
                        sleep(1)
                        rocks.empty()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            #멈췄을 때 화면 블러처리
                            transp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                            transp_surf.set_alpha(200)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('PAUSE',
                                      pygame.font.Font('NanumGothic.ttf', 60),
                                      screen, WINDOW_WIDTH/2, WINDOW_HEIGHT / 2, YELLOW)
                                
                    if event.key == pygame.K_ESCAPE:
                        flag = 1
                        pygame.mixer.music.stop()
                        break
                if event.type == QUIT:
                    return 'quit'

    return'game_screen'

#게임 메인창 만들기
def game_screen():
    global score, flag3
    pygame.mouse.set_visible(True)
    start_image = pygame.image.load('game_screen.png')
    screen.blit(start_image, [0, 0])
    draw_text('avoid meteors',
              pygame.font.Font('NanumGothic.ttf', 70), screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3.4, WHITE)
    draw_text('SCORE : {}'.format(score),
              default_font, screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.5, YELLOW)
    draw_text('The game starts when you click the mouse button or S.'.format(score),
              pygame.font.Font('NanumGothic.ttf', 20), screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WHITE)
    draw_text('Press Q to exit the game.'.format(score),
              pygame.font.Font('NanumGothic.ttf', 20), screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8, WHITE)

    pygame.display.update()

    #키 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return 'play'
            if event.key == pygame.K_q:
                return 'quit'
            if event.key == pygame.K_ESCAPE:
                flag3 = 1
                score = 0
                return 'back'

        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'play'
        if event.type == QUIT:
            return 'quit'
    #게임스크린으로 계속 반복되게 만든다. 
    return 'game_screen'

#메인 루프 설정
def main_loop():
    global flag3, score
    pygame.display.set_icon(pygame.image.load('warp.png'))
    pygame.display.set_caption('Avoid Meteoric')
    action = 'game_screen'
    while action != 'quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            action = game_loop()
        elif action == 'back':
            break

#    pygame.quit() 
#################################################################################################################
def resultProcess():
    global result, win, lose, draw, choiceCom, choiceUser
    choiceCom = random.randint(0, 2)
    if choiceCom == choiceUser:
        result = 0
        draw += 1
    elif (choiceUser == 0 and choiceCom == 1)\
            or (choiceUser == 1 and choiceCom == 2)\
            or (choiceUser == 2 and choiceCom == 0):
        result = 1
        win += 1
    else:
        result = 2
        lose += 1

def setText():
    global result, win, lose, draw
    mFont = pygame.font.SysFont("굴림", 20)
    mtext = mFont.render(f'win {win}, lose {lose}, draw {draw}', True, 'green')
    screen.blit(mtext, (10, 10, 0, 0))

    mFont = pygame.font.SysFont("arial", 15)
    mtext = mFont.render(
        f'(rock : ←) (scissors :  ↑) (paper : →) (continue : space)', True, 'white')
    screen.blit(mtext, (CENTER_WIDTH-40, 10, 0, 0))

    mFont = pygame.font.SysFont("arial", 60)
    mtext = mFont.render(f'VS', True, 'yellow')
    screen.blit(mtext, (CENTER_WIDTH-35, CENTER_HEIGHT-40, 0, 0))

    mFont = pygame.font.SysFont("arial", 40)
    mtext = mFont.render(f'Computer             User', True, 'white')
    screen.blit(mtext, (CENTER_WIDTH-200, CENTER_HEIGHT-100, 0, 0))

    if result != -1:
        mFont = pygame.font.SysFont("arial", 60)
        resultText = ['Draw!!', 'Win!!', 'Lose']
        mtext = mFont.render(resultText[result], True, 'red')
        screen.blit(mtext, (CENTER_WIDTH-80, CENTER_HEIGHT+100, 0, 0))

def getIndex():
    global updateTime, updateIndex
    if result == -1:
        updateTime += 1
        if updateTime > 10:
            updateTime = 0
            updateIndex = (updateIndex+1) % len(player1)
        return updateIndex, updateIndex
    else:
        return choiceCom, choiceUser

def updatePlayer():
    idex1, idex2 = getIndex()

    recPlayer[idex1].centerx = CENTER_WIDTH-100
    recPlayer[idex1].centery = CENTER_HEIGHT
    screen.blit(player1[idex1], recPlayer[idex1])

    recPlayer[idex2].centerx = CENTER_WIDTH+100
    recPlayer[idex2].centery = CENTER_HEIGHT
    screen.blit(player1[idex2], recPlayer[idex2])
###########################################################################################################
class Car:
    #초기화 후, x, y의 좌표값, 차가 어디로 가는지에 대한 좌표값
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        # self.image = pygame.image.load('RacingCar01.png')
        self.image = pygame.image.load('RacingCar02.png')
        #size[0] = width, size[1] = height
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    def draw_image(self):
        #실질적 x, y좌표에 이미지 drop
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        #실제 좌표에 움직이는 방향만큼 더해주기
        self.x += self.dx

    def move_y(self):
        # 실제 좌표에 움직이는 방향만큼 더해주기
        self.y += self.dy

    def check_out_of_screen(self):
        #스크린 넘어가지 않게 만든다.
        #윈도우 창의 오른쪽 끝 or 왼쪽 끝
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx

    def check_crush(self, car):
        #내 자동차와 타차가 부딫혔는가
        if(self.x + self.width > car.x) and (self.x < car.x+car.width) and\
                (self.y < car.y+car.height) and (self.y+self.height > car.y):
            return True
        else:
            return False

def draw_main_menu():
    global flag4, space
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('PyCar.png')
    screen.blit(image_intro, [draw_x, draw_y - 300])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render('Racing Car Game', True, BLACK)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render("Score: "+str(score1), True, WHITE)
    screen.blit(text_score, [draw_x, draw_y + 170])
    text_start = font_30.render("Press Spacebar X2 to START", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 240])
    text_start = font_30.render("Press left/right key to play", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 280])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = 1
                break
            if event.key == pygame.K_ESCAPE:
                flag4 = 1
                break
            if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    pygame.display.flip()

def draw_score():
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_score = font_30.render("Score: " + str(score1), True, BLACK)
    screen.blit(text_score, [15, 15])
    
player = Car(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200, 0, 0)
player.load_image()

cars = []
car_count = 3
for i in range(car_count):
    #자동차가 나오는 곳을 랜덤하게 정함.
    x = random.randrange(0, WINDOW_WIDTH - 55)
    y = random.randrange(-150, -50)
    #속도를 5~10 사이로 정의함.
    car = Car(x, y, 0, random.randint(3, 8))
    car.load_image()
    cars.append(car)

lanes = []
#차선 그리기,
lane_width = 10
lane_height = 80
lane_margin = 20
lane_count = 20
lane_x = (WINDOW_WIDTH - lane_width / 2)
lane_y = -10
for i in range(lane_count):
    lanes.append([lane_x, lane_y])
    lane_y += lane_height + lane_margin

score1 = 0
crash = True
###############################################################################################################
    
def runGame():
    global d_count, s_num, s_shot, s_explode, s_destroy, screen, scr, screen_width, screen_height, select_sound,\
    player, rectPlayer, star, rectStar, score,\
    choiceUser, choiceCom, result, win, lose, draw,\
    sound_racing, sound_crush, sound_engine, crash, space, score1,\
    flag1, flag2, flag3, flag4
    
    missile_xy = []
    
    x = screen_width * 0.4
    y = screen_height * 0.75
    x_change = 0
    
    asteroid_x = random.randrange(0, screen_width - asteroid_width)
    asteroid_y = 0
    asteroid_speed = 4

    done = False    
    
    while not done:
        for event in pygame.event.get():
            if scr == 0:
                screen = pygame.display.set_mode((screen_width, screen_height))
                select()
                select_sound.play(-1)
                select_sound.set_volume(0.5)
                if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                        
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1]: scr = 1
                elif pressed[pygame.K_2]: scr = 2
                elif pressed[pygame.K_3]: scr = 3
                elif pressed[pygame.K_4]: scr = 4
                elif pressed[pygame.K_5]: scr = 5
                elif pressed[pygame.K_q]: 
                    pygame.quit()
                    sys.exit()
####################################################################################################################                
            if scr == 1: 
                select_sound.stop()
                rock_sound.play(-1)
                rock_sound.set_volume(0.2)
                pygame.display.set_icon(pygame.image.load('rock.png'))
                pygame.display.set_caption('ROCK SCISSORS PAPER')
                while True:
                    screen_width = 700
                    screen_height = 400
                    if flag1 == 1:
                        flag1 = 0
                        scr = 0
                        result, choiceUser, choiceCom = -1, -1, -1
                        win, lose, draw = 0, 0, 0
                        rock_sound.stop()
                        screen_width = 800
                        screen_height = 600
                        break
                    for event in pygame.event.get():
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        screen.fill((0, 0, 0))
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                flag1 = 1
                                break
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                            if result == -1:
                                if event.key == pygame.K_LEFT:  # 바위
                                    choiceUser = 0
                                if event.key == pygame.K_UP:  # 가위
                                    choiceUser = 1
                                if event.key == pygame.K_RIGHT:  # 보
                                    choiceUser = 2
                                if choiceUser != -1:
                                    resultProcess()
                            else:
                                if event.key == pygame.K_SPACE:  # 재시작
                                    result, choiceUser, choiceCom = -1, -1, -1
            
                    updatePlayer()
                    setText()
                    pygame.display.flip()
                    clock.tick(100)
####################################################################################################################            
            if scr == 2:
                select_sound.stop()
                pygame.display.set_icon(pygame.image.load('shuttle.png'))
                pygame.display.set_caption('Destroy Meteoric')
                while True:
                    screen_width = 480
                    screen_height = 640
                    if flag2 == 1:
                        flag2 = 0
                        scr = 0
                        d_count = 0
                        s_num = 3
                        screen_width = 800
                        screen_height = 600
                        break
                    for event in pygame.event.get():
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        if event.type == pygame.QUIT:
                                done = True
                                pygame.quit()
                                sys.exit()
                
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                x_change -= 10
                                x += x_change
                                x_change = 0
                            if event.key == pygame.K_RIGHT:
                                x_change += 10
                                x += x_change
                                x_change = 0
                            if event.key == pygame.K_SPACE:
                                s_shot.play()
                                s_shot.set_volume(0.1)
                                if len(missile_xy) < 6:
                                    missile_x = x + shuttle_width/2 - 12
                                    missile_y = y - shuttle_height/4
                                    missile_xy.append([missile_x, missile_y])
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                            if event.key == pygame.K_ESCAPE:
                                flag2 = 1
                                break
            
                    screen.blit(background, (0, 0))
            #        screen.fill((255, 255, 255))        
                    
                    if x < 0:
                        x = 0
                    elif x > screen_width - shuttle_width:
                        x = screen_width - shuttle_width
                        
                    if y < asteroid_y + asteroid_height - 20:
                        if asteroid_x > x-60 and asteroid_x < x + shuttle_width-20:
                            s_explode.play()
                            s_explode.set_volume(0.3)
                            s_num -= 1
                            if s_num != 0:
                                explode()
                            
                    if s_num == 0:
                        gameOver()
                    if d_count == 100:
                        gameOver()
                        
                    drawObject(shuttle, x, y)
                    
                    if len(missile_xy) != 0:
                        for i, bxy in enumerate(missile_xy):
                            bxy [1] -= 10
                            missile_xy[i][1] = bxy[1]
                            if bxy[1] < asteroid_y:
                                if bxy[0] > asteroid_x and bxy[0] < asteroid_x + asteroid_width:
                                    missile_xy.remove(bxy)
                                    asteroid_x = random.randrange(0, screen_width - asteroid_width)
                                    asteroid_y = 0
                                    d_count += 10
                                    s_destroy.set_volume(0.3)
                                    s_destroy.play()
                                   
                                    
                            if bxy[1] <= 0:
                                try:
                                    missile_xy.remove(bxy)
                                except:
                                    pass
                    if len(missile_xy) != 0:
                        for bx, by in missile_xy:
                            drawObject(missile, bx, by)
                            
                    showScore(d_count, s_num)
                    
                    asteroid_y += asteroid_speed
                    if asteroid_y > screen_height:
                        asteroid_y = 0
                        asteroid_x = random.randrange(0, screen_width - asteroid_width)
                        
                    drawObject(asteroid, asteroid_x, asteroid_y)
                    pygame.display.flip()
                    pygame.display.update()
                    clock.tick(60)
####################################################################################################################                    
            if scr == 3:
                select_sound.stop()
                screen_width = 800
                screen_height = 600
                screen = pygame.display.set_mode((screen_width, screen_height))
                if flag3 == 1:
                    flag3 = 0
                    scr = 0
                else: 
                    main_loop()
####################################################################################################################
            if scr == 4:
                select_sound.stop()
                pygame.display.set_icon(pygame.image.load('PyCar.png'))
                pygame.display.set_caption('Car Racing')
                while True:
                    screen_width = 800
                    screen_height = 700
                    if flag4 == 1:
                        flag4 = 0
                        scr = 0
                        score1 = 0
                        screen_width = 800
                        screen_height = 600
                        sound_racing.stop()
                        sound_engine.stop()
                        crash = True
                        space = 0
                        break
                    #이벤트 처리.
                    for event in pygame.event.get():
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                
                        if crash:
                            #충돌하면 게임이 다시 시작될 수 있는 요소를 줄 것임
                            if space == 1:
                                crash = False
                                for i in range(car_count):
                                    cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                                    cars[i].y = random.randrange(-150, -50)
                
                
                                player.load_image()
                                player.x = WINDOW_WIDTH / 2
                                player.dx = 0
                                score1 = 0
                                pygame.mouse.set_visible(False)
                                sound_engine.play()
                                sleep(1)
                                sound_racing.play(-1)
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                flag4 = 1
                                break
                        if not crash:
                            #키가 눌렸을때
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RIGHT:
                                    player.dx = 4
                                if event.key == pygame.K_LEFT:
                                    player.dx = -4
                                if event.key == pygame.K_ESCAPE:
                                    sound_racing.stop()
                                    sound_engine.stop()
                                    crash = True
                                    space = 0
                                if event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
                
                            #키에 안 눌릴때
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_RIGHT:
                                    player.dx = 0
                                elif event.key == pygame.K_LEFT:
                                    player.dx = 0
                
                    screen.fill(GRAY)
                
                    if not crash:
                        for i in range(lane_count):
                            #차선을 계속 그린다.
                            pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                            lanes[i][1] += 10
                            if lanes[i][1] > WINDOW_HEIGHT:
                                #전체 게임 화면을 차선이 넘어갔을 때
                                lanes[i][1] = -40 - lane_height
                
                        player.draw_image()
                        player.move_x()
                        player.check_out_of_screen()
                
                        for i in range(car_count):
                            cars[i].draw_image()
                            #플레이어는 좌우로, 상대방들은 위에서 아래로 움직인다.
                            cars[i].y += cars[i].dy
                            if cars[i].y > WINDOW_HEIGHT:
                                score1 += 10
                                cars[i].x = random.randint(0, WINDOW_WIDTH - cars[i].width)
                                cars[i].y = random.randint(-150, -50)
                                cars[i].dy = random.randint(3, 8)
                                cars[i].load_image()
                
                        for i in range(car_count):
                            #플레이어가 타차랑 부딫히면 일어나게 되는 것들.
                            if player.check_crush(cars[i]):
                                crash = True
                                sound_racing.stop()
                                sound_engine.stop()
                                #노래 멈추기, 잠깐 멈추고, 마우스 보이게 된다.
                                sound_crush.play()
                                sleep(1)
                                pygame.mouse.set_visible(True)
                                space = 0
                                break
                        #점수 표출
                        draw_score()
                        pygame.display.flip()
                
                    else:
                        draw_main_menu()
                
                    clock.tick(60)
####################################################################################################################                    
            if scr == 5:
                    
                    window=tkinter.Tk()
                    ####
                    select_sound.stop()
                    lbl = Label(window, text="이름") 
                    lbl.pack()
                    ##### 배경음악
                    mixer.init()##mixer초기화
                    mixer.music.load("Itro.mp3")#음악 파일 로드
                    mixer.music.play(-1)# 음악 재생 -1을 넣어주면 무한반복
                    
                    base = PhotoImage(file = "base2.gif")#배경화면 이미지 지정
                    base_label = Label(image = base)#
                    base_label.place(x = 0, y = 0)#사진의 위치 지정
                    ##글자를 입력받을 텍스트위젯
                    ## 이름을 입력받게 하여 게임이 끝난 후 이름과 
                    ## 횟수등을 저장할 예정
                    txt = Text(window,width=20,height=2 )
                    txt.pack()
                    txt.insert(END,"이름을 입력하세요")
                    ## 세이브 버튼 
                    def btnsave():
                        print(txt.get("1.0",END))##1:첫번째 라인 , 0 : 0번째 colum 위치 END는 끝까지
                        global userName ## scope가 달라 global로 지정해주지 않으면 전역 변수가 아닌 
                        #지역변수를 사용하려 하여 에러가 난다. 
                        userName+=txt.get("1.0",END)
                        txt.delete("1.0",END) # 텍스트 상자에 있던 내용 삭제.
                    btn = Button(window,text="save",command=btnsave) 
                    btn.pack()  
                    ############################
                    ##menu탭에 실행하기 추가!!!
                    def RunStrike():
                        global cnt
                        global com 
                        strike_count =0
                        bol_count =0
                        cnt +=1
                        for i in range(0,3):
                            if (com[i] == user[i]): ## 같은 자리 같은 숫자면 스트라이크 증가
                                strike_count=strike_count+1
                            else:
                                j=0
                                for j in range(0,3):
                                    if (com[i] == user[j]):
                                        bol_count = bol_count + 1
                        messagebox.showinfo("yes", "%d스트라이크" % strike_count)
                        messagebox.showinfo("yes", "%d볼" % bol_count) 
                        if(com==user):
                            messagebox.showinfo("yes", "%d 번만에 정답!!" % cnt)
                            window.quit()
                            window.destroy()
                            pygame.quit()
                            sys.exit()
                            
                    def Close():
                        window.quit()
                        window.destroy()        
                        pygame.quit()
                        sys.exit()
      
                    def Init():
                        user.clear()
                        
                    menubar = Menu(window)
                    
                    menu1 = Menu(menubar, tearoff=0)
                    menu1.add_command(label="실행",command=RunStrike)
                    menu1.add_separator()
                    menu1.add_command(label="Exit", command=Close)
                    menubar.add_cascade(label="File", menu=menu1)
                    
                    menu2 = Menu(menubar, tearoff=0, selectcolor="red")
                    menu2.add_command(label="초기화", command =Init)
                    menubar.add_cascade(label="Edit", menu=menu2)
                    window.config(menu=menubar)
                    ##################################33
                    while True: 
                        rd = random.randint(1, 9)
                        if(not rd in com):
                            com.append(rd)
                            if len(com) == 3:
                                break 
#                    print(com)
                    cnt=0 ##게임 횟수 저장변수
                    #######타이틀 작성 
                    window.title("Strike")
                    window.geometry("640x400+100+100")
                    window.resizable(False, False)
                    ########## 공지사항 출력. 
                    label=tkinter.Label(window, text="1) 이름을 입력 후 'save'를 클릭하세요!\n2) 겹치지 않는 숫자 3개 선택 후 'File -> 실행'\n3) 계속 도전하려면 'Edit -> 초기화'")
                    label.pack()
                    
                    #### 이미지 버튼 함수.
                    def ClickNum(n):
                        if len(user)<3:
                            user.append(int(n))
                            messagebox.showinfo("yes", "숫자{}이 입력됩니다".format(n))
                    
                    ####################################
                    for i in range(1,10):
                        globals()['photo{}'.format(i)] = PhotoImage(file="./"+str(i)+".gif",master=window)
                
                    lbl1 = Button(window, image=photo1,command = lambda: ClickNum(1))
                    lbl2 = Button(window, image=photo2,command = lambda: ClickNum(2))
                    lbl3 = Button(window, image=photo3,command = lambda: ClickNum(3))
                    lbl4 = Button(window, image=photo4,command = lambda: ClickNum(4))
                    lbl5 = Button(window, image=photo5,command = lambda: ClickNum(5))
                    lbl6 = Button(window, image=photo6,command = lambda: ClickNum(6))
                    lbl7 = Button(window, image=photo7,command = lambda: ClickNum(7))
                    lbl8 = Button(window, image=photo8,command = lambda: ClickNum(8))
                    lbl9 = Button(window, image=photo9,command = lambda: ClickNum(9))
                    
#                   for i in range(1,10):
#                        globals()['lbl{}'.format(i)].pack(side=LEFT)
                    lbl1.pack(side=LEFT)
                    lbl2.pack(side=LEFT)
                    lbl3.pack(side=LEFT)
                    lbl4.pack(side=LEFT)
                    lbl5.pack(side=LEFT)
                    lbl6.pack(side=LEFT)
                    lbl7.pack(side=LEFT)
                    lbl8.pack(side=LEFT)
                    lbl9.pack(side=LEFT)
                 
                    window.protocol('WM_DELETE_WINDOW',Close)
                    window.mainloop()

                    
        pygame.display.flip()


          
startGame()
runGame()
