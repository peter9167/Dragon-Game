'''
제목 : 파이썬 익룡 슈팅 게임 버전 1.0
날짜 : 2021 / 07/ 28 ~
프로그래머 : 이진영
'''

import pygame
import sys
import random
from time import sleep
import timeit

#BLACK = (0, 0, 0)     #배경 색상 : 검정
padWidth = 480
padHeight = 640
gameTitle = "파이썬 게임"

rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png',\
             'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png','rock10.png',\
             'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png',\
             'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png',\
             'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png',\
             'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock20.png',]

rockImage2 = []

#게임 사용 사운드(뮤직, 음악) 호출
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']

#사용자 함수를 선언한다.
#게임 메세지 출력 함수 선언
def writeMessage(text):
    global gamePad, gameOverSound, time_count

    textfont = pygame.font.Font('NanumGothic.ttf', 60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()

    pygame.mixer.music.stop()
    gameOverSound.play()

    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

#전투기가 운석에 충돌 했을 때 --> 전투기 파괴
def f_crash():
    global gamePad
    writeMessage('익룡 파괴')

def gameOver():
    global gamePad
    writeMessage('익룡 게임 오버')


#운석을 맞춘 갯수 계산 함수
def writeShotScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20) #font 클래스에 Font함수 호출해서 나눔 고딕으로 폰트 설정
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    #text 변수 안에 font 클래스를 이용해서 render 함수 호출해서 출력
    #reder(출력 내용(str형), 텍스트 표시 상태, 글자 색)
    gamePad.blit(text, (10, 0))

#운석을 맞추지 못한 갯수 계산 함수
def writePassScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20) #font 클래스에 Font함수 호출해서 나눔 고딕으로 폰트 설정
    text = font.render('놓친 운석수:' + str(count), True, (255, 0, 0))
    #text 변수 안에 font 클래스를 이용해서 render 함수 호출해서 출력
    #reder(출력 내용(str형), 표시 상태, 글자 색)
    gamePad.blit(text, (350, 0))

#운석 스피드 계산 함수
def writeSpeedScore(speed):
    global gamePad

    font = pygame.font.Font('NanumGothic.ttf', 20) #font 클래스에 Font함수 호출해서 나눔 고딕으로 폰트 설정
    text = font.render('운석 스피드:' + str(int(speed)), True, (64, 244, 208))
    #text 변수 안에 font 클래스를 이용해서 render 함수 호출해서 출력
    #reder(출력 내용(str형), 표시 상태, 글자 색)
    gamePad.blit(text, (10, 600))

#게임 시간 계산 함수
def writeTimeScore(time):
    global gamePad

    font = pygame.font.Font('NanumGothic.ttf', 20) #font 클래스에 Font함수 호출해서 나눔 고딕으로 폰트 설정
    text = font.render('게임시간:' + str(int(time)), True, (255, 255, 255))
    #text 변수 안에 font 클래스를 이용해서 render 함수 호출해서 출력
    #reder(출력 내용(str형), 표시 상태, 글자 색)
    gamePad.blit(text, (10, 25))

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, background2, fighter, missile, explosion, missileSound, gameOverSound, time_count

    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption(gameTitle)
    clock = pygame.time.Clock()

    background = pygame.image.load('background.png')
    background2 = pygame.image.load('background2.png')
    fighter = pygame.image.load('drangon.png')
    missile = pygame.image.load('fireboll.png')
    explosion = pygame.image.load('explosion.png')

    pygame.mixer.music.load('music.wav') #배경 음악
    pygame.mixer.music.play(-1) #배경 음악 재생
    missileSound = pygame.mixer.Sound('missile.wav')
    gameOverSound = pygame.mixer.Sound('gameover.wav')


def runGame():
    global gamePad, clock, background, background2, fighter, missile, rock, explosion, missileSound, time_count

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    fx = padWidth * 0.45 #비행기에 좌표 x값을 갖는 변수
    fy = padHeight * 0.9
    fighterX = 0 #화면에 표시되는 변수
    fighterY = 0

    #미사일 화면에 표시하는 리스트형 변수(선언)
    missileXY = []

    #운석을 화면에 표시하는 변수 만들기(선언
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    #운석의 초기 X위치 설정한다.
    rockX = random.randrange(0, padWidth - rockWidth)
    # 운석의 초기 Y위치 설정한다.
    rockY = 0
    rockSpeed = 2 #운석 떨어지는 속도 변수


    okShot = False # 전투기 미사일에 운석이 맞았을 경우 변수 선언
    shotCount = 0 #운석을 맞췄을 때 카운트 변수
    rockPassed = 0 #운석을 맞추지 못했을 때 카운트 변수

    onGame = True #게임 계속 실행
    while onGame:
        time_count = timeit.default_timer()  # 시작 시간 체크
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()
            # 방향키 제어 변수
            if event.type in [pygame.KEYDOWN]:  # 키가 눌려 졌을때
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_UP:
                    fighterY -= 5

                elif event.key == pygame.K_DOWN:
                    fighterY += 5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = fx + fighterWidth / 2
                    missileY = fy -fighterHeight
                    missileXY.append([missileX, missileY])

            #스페이스 키 제어 변수
            if event.type in [pygame.KEYUP]:  # 키가 떼어 졌을때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterX = 0
                    fighterY = 0

        if shotCount >= 20:
            drawObject(background2, 0, 0)  # 배경 출력
        elif shotCount >= 40:
            drawObject(background2, 0, 0)  # 배경 출력

        drawObject(background, 0, 0)  # 배경 출력

        fx += fighterX
        fy += fighterY
        if fx < 0:
            fx = 0
        elif fx > padWidth - fighterWidth:
            fx = padWidth - fighterWidth
        if fy < 0:
            fy = 0
        elif fy > padHeight - fighterHeight:
            fy = padHeight - fighterHeight

        # 익룡이 운석에 맞았는지 검사하는 부분
        if fy < rockY + rockHeight:
            if (rockX > fx and rockX < fx + fighterWidth) or \
                    (rockX + rockWidth > fx and rockX + rockWidth < fx + fighterWidth):
                f_crash()

        drawObject(fighter, fx, fy)  # 비행기 출력

        if len(missileXY) != 0: #화면 끝, Y좌표가 0이 되지 않으면 실행 코드
            for i, bxy in enumerate(missileXY): #missileXY값을 i, bxy 값으로 튜플형태로 반환
                #enumerate:인덱스 번호와 컬렉션의 원소를 tuple형태로 반환합니다.
                bxy[1] -= 10
                #bxy[1]값 = by값과 같다. 그러니깐 미사일Y값을 지정해주기 bxy를 선언
                #그래서 bxy에 by값에 -= 10을 한거
                missileXY[i][1] = bxy[1] #최종적으로 미사일Y값에 bxy[1]을 넣어준다.

                if bxy[1] < rockY: #bxy[0] = bx값과 같다.
                    '''
                    미사일 Y좌표 값이 운석 Y좌표값보다 더 커지면
                    bxy[0]값이 운석 X좌표 값보다 크고 
                    운석 X좌표 값과 운석 이미지 크기 더한 값이 bxy[0]값이 더 작다면
                    '''
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy) #미사일 좌표 삭제
                        okShot = True #okShot True로 정의하면서 맞았다는 신호 보내서 어디선가 신호를 받음
                        shotCount += 1 #점수 카운트 + 1

                if bxy[1] <= 0: #bxy[1]이 0보다 작으면
                    try:
                        missileXY.remove(bxy) #bxy값 삭제
                    except: #오류나면 실행해야 되는데 솔직히 try이가 코드 한줄인데 오류나겠냐?
                        pass #그러니깐 그냥 킵

        if len(missileXY) != 0:
            for bx, by in missileXY: #미사일 이미지 출력 코드 알쥐?
                drawObject(missile, bx, by)

        writeShotScore(shotCount)

        rockY += rockSpeed #이거 없으면 미사일 안움직임. 일단 rockY값에 rockSpeed 값넣어서 2씩 증가


        if rockY > padHeight: #운석이 화면을 넘어가면, 화면 좌표보다 커지면
            rock = pygame.image.load(random.choice(rockImage)) #이미지 로드
            rockSize = rock.get_rect().size #운석 사이즈 변수
            rockWidth = rockSize[0] #운석 가로 사이즈 변수
            rockHeight = rockSize[1] #운석 세로 사이즈 변수

            rockX = random.randrange(0, padWidth - rockWidth) #random 함수를 이용하여 rockX좌표 랜덤으로 저장
            rockY = 0 # rockY 좌표는 0으로 하면서 계속 떨어질 수 있도록
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        #놓친 운석수 표시
        writeSpeedScore(rockSpeed)
        writeTimeScore(time_count)

        writePassScore(rockPassed)

        if okShot == True:
            drawObject(explosion, rockX, rockY)

            #새로운 운석 가져오기
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

            okShot = False

            # 운석을 맞추면 운석의 속도를 증가한다.
            rockSpeed += 0.2
            if rockSpeed > 10:
                rockSpeed = 10
        drawObject(rock, rockX, rockY)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()