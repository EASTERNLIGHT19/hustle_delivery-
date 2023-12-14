import pygame
import random
import time
import os
import sys

# 이미지 폴더 경로 지정
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "image")

pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()
game_run = True

# 배경 음악 로드 및 재생
pygame.mixer.music.load(os.path.join(image_path, "pygame_bgm.wav"))
# pygame.mixer.music.load(os.path.join(image_path, "pygame_bgm.wav"))
pygame.mixer.music.play(-1)  # -1은 반복 재생을 의미합니다.

# 화면 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hustle Delivery")
FPS = 60

# 게임 상태
# main, information, main_game, doorbell_gmae, balloon_game, jump_game, death_screen
game_status = 'main'

Black = (0, 0, 0)
White = (255, 255, 255)
Blue = (0, 0, 180)


def text_object(text, font):
    text_surface = font.render(text, True, Black)
    return text_surface, text_surface.get_rect()


class Button:
    def __init__(self, txt, x, y, width, hight, color, over_color, font_size):
        global game_status
        global mouse
        global click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.txt = txt
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.color = color
        self.over_color = over_color
        self.font_size = font_size

        pygame.draw.rect(screen, self.color, [ self.x, self.y, self.width, self.hight])

        text_size = pygame.font.SysFont("malgungothic", self.font_size)
        text_surf, text_rect = text_object(self.txt, text_size)
        text_rect.center = ((self.x + (self.width / 2)),(self.y + (self.hight / 2)))
        screen.blit(text_surf, text_rect)

    def action(self, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.width > mouse[0] > self.x and self.y + self.hight > mouse[1] > self.y:
            pygame.draw.rect(screen, self.over_color, [ self.x, self.y, self.width, self.hight])
            if click[0] == 1:
                action()
        else:
            pygame.draw.rect(screen, self.color, [ self.x, self.y, self.width, self.hight])

        text_size = pygame.font.SysFont("malgungothic", self.font_size)
        text_surf, text_rect = text_object(self.txt, text_size)
        text_rect.center = ((self.x + (self.width / 2)),(self.y + (self.hight / 2)))
        screen.blit(text_surf, text_rect)


def click_main():
    global game_status
    game_status = 'main'


def click_main_game():
    global game_status
    game_status = 'main_game'


def click_information():
    global game_status
    game_status = 'information'


middle_crow_hit = 0
high_crow_hit = 0
hole_hit = 0
house_hit = 0

double_touch = True
obstacles_speed = None
minigame_hit = 0
score = 0
doorbell_game_count = 0
arrow_image = None
hit = 0
doorbell_game_total_time = 0
doorbell_game_start_time = 0

information_image = pygame.image.load(
    os.path.join(image_path, "information_image.png"))

# man 정의


class man(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(image_path, "man.png"))
        self.image = pygame.transform.scale(
            self.image, (70, 70))  # 이미지 크기를 70,70으로 지정
        self.rect = self.image.get_rect()  # 모양을 이미지로 지정
        self.rect.topleft = (100, 300)  # 위치를 왼쪽에서 100, 밑에서 70의 위치로 지정
        self.jump_pow = 0  # 매틱 이동할 거리
        self.jump = None  # 점프가 된 시간
        self.jump_time = 200  # 최대 점프 시간

    def jump_update(self):
        if self.jump is None:  # 처음으로
            self.jump = pygame.time.get_ticks()  # 현재 틱을 점프에 저장
            self.jump_pow += 1  # 점프파워 증가
        # 현재 시간-점프한시간 이 점프 최대시간보다 작으면 == 점프 최대시간을 안넘겼으면
        elif pygame.time.get_ticks() - self.jump <= self.jump_time:
            self.jump_pow += 1  # 점프파워 증가

    def jump_reset(self):  # 땅에 닿았을 경우 작동
        self.jump_pow = 0  # 점프거리 초기화
        self.jump = None  # 점프시간 초기화

    def draw(self, surface):  # 그리기
        surface.blit(self.image, self.rect)

    def move(self):
        self.rect.y -= self.jump_pow  # jump_pow만큼 이동
        if self.jump != None:  # 점프가 활성화일때
            if pygame.time.get_ticks() - self.jump > self.jump_time:  # 현재 시간-점프한시간 이 점프 촤대시간보다 크면 == 점프 최대시간을 넘겼으면
                self.jump_pow -= 1  # 점프파워 감소

        if self.jump != None and self.rect.y > HEIGHT - 100:  # 점프가 비활성화고, 바닥에 닿으면
            self.rect.y = HEIGHT - 100  # 높이를 바닥높이로 지정
            self.jump_reset()  # 점프관련 변수 리셋


# high_crow정의
class high_crow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = "high_crow"
        self.image = pygame.image.load(os.path.join(image_path, "crow.png"))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 200

    def update(self):
        if game_status == 'main_game':
            self.rect.x = self.rect.x - obstacles_speed

    def hit_scan(self):
        global high_crow_hit
        if self.rect.x <= 165 and self.rect.x >= 100:
            high_crow_hit = 1
        if (self.rect.x + 60) <= 165 and (self.rect.x + 60) >= 100:
            high_crow_hit = 1


# middle_crow정의
class middle_crow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = "middle_corw"
        self.image = pygame.image.load(os.path.join(image_path, "crow.png"))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 300

    def update(self):
        if game_status == 'main_game':
            self.rect.x = self.rect.x - obstacles_speed

    def hit_scan(self):
        global middle_crow_hit
        if self.rect.x <= 165 and self.rect.x >= 100:
            middle_crow_hit = 1
        if (self.rect.x + 60) <= 165 and (self.rect.x + 60) >= 100:
            middle_crow_hit = 1


# hole정의
class Hole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = "Hole"
        self.image = pygame.image.load(os.path.join(image_path, "hole.png"))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 320

    def update(self):
        if game_status == 'main_game':
            self.rect.x = self.rect.x - obstacles_speed

    def hit_scan(self):
        global hole_hit
        if 100 <= self.rect.x <= 165:
            hole_hit = 1
        if 100 <= (self.rect.x + 60) <= 165:
            hole_hit = 1


# house정의
class house(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = "house"
        self.image = pygame.image.load(os.path.join(image_path, "house.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 300

    def update(self):
        if game_status == 'main_game':
            self.rect.x = self.rect.x - obstacles_speed

    def hit_scan(self):
        global house_hit
        if 100 <= self.rect.x <= 175:
            house_hit = 1
        if 100 <= (self.rect.x + 70) <= 175:
            house_hit = 1


# doorbell_game 진입
doorbell_game_bg = pygame.image.load(os.path.join(image_path, "door.png"))
up_image = pygame.image.load(os.path.join(image_path, "up.png"))
down_image = pygame.image.load(os.path.join(image_path, "down.png"))
left_image = pygame.image.load(os.path.join(image_path, "left.png"))
right_image = pygame.image.load(os.path.join(image_path, "right.png"))

up = pygame.K_UP
down = pygame.K_DOWN
left = pygame.K_LEFT
right = pygame.K_RIGHT
bell = None

bell_type = [up, down, left, right]

score_size = pygame.font.SysFont("malgungothic", 62)


player = man()  # man클래스의 player객체 생성
house0 = house()


# 장해물 부딛힘 판정
def man_hit_scan(player_y):
    global hit
    global minigame_hit
    global double_touch
    global player

    global hole_hit
    global middle_crow_hit
    global high_crow_hit
    global house_hit

    # 높은 까마귀 접촉 판정
    if high_crow_hit == 1:
        # print("hc active")
        if player_y >= 200 and player_y <= 260:
            hit = 1
        if (player_y + 70) >= 200 and (player_y + 70) <= 260:
            hit = 1

    # 중간 까마귀 접촉 판정
    if middle_crow_hit == 1:
        # print("mc active")
        if player_y >= 300 and player_y <= 360:
            hit = 1
        if (player_y + 70) >= 300 and (player_y + 70) <= 360:
            hit = 1

    # 맨홀 접촉 판정
    if hole_hit == 1:
        # print("ho active")
        if (player_y + 70) >= 320:
            hit = 1

    # 집 접촉 판정
    if house_hit == 1 and double_touch == True:
        if (player_y + 70) >= 300 and (player_y + 70) <= 370:
            minigame_hit = random.randrange(1, 4)
            double_touch = False


sprites = [player]
sprite_group = pygame.sprite.RenderPlain(*sprites)

enemy = None
enemy_type = None


def add_sprite(sprite_type):
    global enemy_type
    global enemy
    # print(sprite_type)
    if sprite_type == 1:
        enemy = Hole()
        enemy_type = "hole"
    elif sprite_type == 2:
        enemy = high_crow()
        enemy_type = "hc"
    elif sprite_type == 3:
        enemy = middle_crow()
        enemy_type = "mc"
    elif sprite_type == 4:
        enemy = house()
        enemy_type="house"

    if len(sprites) == 2:  # 다른 스프라이트가 있을때
        sprites[1] = enemy
    elif len(sprites) == 1:  # 플레이어만 있을때
        sprites.append(enemy)


    global sprite_group
    sprite_group = pygame.sprite.RenderPlain(*sprites)


gen_tick = 0


#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################

while game_run == True:

    if game_status == 'main':
        obstacles_speed = 5  # 초기 장해물 속도 설정
        score = 0  # 초기 스코어 설정

        # 장해물 접촉 판정 값 초기화
        # 1일 경우 man과 장해물 들의 이미지가 x축에서 겹침

        middle_crow_hit = 0
        high_crow_hit = 0
        hole_hit = 0
        house_hit = 0

        # 까마귀 또는 맨홀에 접촉하면 1로 바뀜
        hit = 0

        screen.fill(White)  # 배경을 하얀색으로 채우기
        btn_start_game = Button("게임 시작", 400, 150, 140, 70, White, Blue, 36)
        btn_game_info = Button("게임 설명", 400, 250, 140, 70, White, Blue, 36)

        while game_status == 'main':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # print('mouse is move')
                    btn_start_game.action(click_main_game)
                    btn_game_info.action(click_information)
                elif event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(FPS)
            pygame.display.update()

    if game_status == 'information':
        screen.blit(information_image, (0, 0))

        btn_main = Button("메인 화면", 40, 20, 70, 35, White, Blue, 14)
        while game_status == 'information':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    btn_main.action(click_main)
                elif event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(FPS)
            pygame.display.update()

    if game_status == 'main_game':
        minigame_hit = 0  # 집에 접촉하면 1~3 으로 바뀜
        double_touch = True  # 집 연속 터치 방지,True=터치 가능, False=터치 불가
        sprites = [player]  # 스프라이트 그룹에 플레이어만 있게 변경
        sprite_group = pygame.sprite.RenderPlain(*sprites)
        gen_tick = pygame.time.get_ticks()

        enemy = None
        enemy_type = None

        start_time = pygame.time.get_ticks()

        # 메인 게임 동안
        while game_status == 'main_game':
            screen.fill(White)  # 배경을 하얀색으로 채우기
            # 배경 채우기가 없을 경우 플레이어의 잔상이 남음

                # 미니게임 진입
            if minigame_hit == 1:
                game_status = 'doorbell_game'
            elif minigame_hit == 2:
                game_status = 'balloon_game'
            elif minigame_hit == 3:
                game_status = 'jump_game'

            if double_touch == False:
                time.sleep(1)
                double_touch = True

            now_tick = pygame.time.get_ticks()  # 계속 갱신되는 현재 틱
            obstacles_speed = obstacles_speed + ((now_tick-start_time) / 3000000)

            if now_tick-gen_tick > 2000:
                add_sprite(random.randrange(1,5))  # 적을 생성
                gen_tick = now_tick

            player.move()  # 플레이어의 위치 변경
            clock.tick(FPS)  # 틱 제한
            sprite_group.update()
            sprite_group.draw(screen)

            if enemy_type != None:
                enemy.hit_scan()
                enemy.update()

            man_hit_scan(player.rect.y)

            # 가로 충돌 초기화
            hole_hit = 0
            middle_crow_hit = 0
            high_crow_hit = 0
            house_hit = 0

            key_event = pygame.key.get_pressed()  # 눌린 키 가져오기
            if key_event[pygame.K_SPACE]:  # 스페이스바가 눌렸을때
                player.jump_update()  # 점프 업데이트 함수 작동

            for event in pygame.event.get():  # 이벤트 활성화시
                if event.type == pygame.QUIT:
                    pygame.quit()

            # 부딛힘 시 게임 오버
            if hit == 1:
                game_status = 'death_screen'

            pygame.display.update()  # 화면 업데이트

    # doorbell_game 진입
    if game_status == 'doorbell_game':
        doorbell_game_total_time = 5
        doorbell_game_start_time = pygame.time.get_ticks()
        bell = random.choice(bell_type)
        arrow_image = None
        doorbell_game_count = 0

        if bell == up:
            arrow_image = up_image
        if bell == down:
            arrow_image = down_image
        if bell == left:
            arrow_image = left_image
        if bell == right:
            arrow_image = right_image

        while game_status == 'doorbell_game':

            double_touch=False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == bell:
                        doorbell_game_count = doorbell_game_count + 1
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.blit(doorbell_game_bg, (0, 0))
            screen.blit(arrow_image, (325, 110))

            game_font = pygame.font.Font(None, 40)
            doorbell_game_run_time = (pygame.time.get_ticks() - doorbell_game_start_time) / 1000
            doorbell_game_timer = game_font.render("Timer:" + str(int(doorbell_game_total_time - doorbell_game_run_time)), True, (255, 255, 255))
            screen.blit(doorbell_game_timer, (10, 10))
            pygame.display.update()

            if (doorbell_game_total_time - doorbell_game_run_time) <= 0:
                game_status = 'main_game'

            if doorbell_game_count == 5:
                arrow_image = None
                bell = None
                score = score + 1
                game_status = 'main_game'
                doorbell_game_count = 0 

    # balloon_game 진입
    if game_status == 'balloon_game':
        image_bg = pygame.image.load("image/house_bg.png")    # 이미지 변수 대입
        image_balloon = pygame.image.load("image/balloon.png")
        image_broken = pygame.image.load("image/pop.png")

        size_bg_width = screen.get_size()[0]     #배경화면의 x사이즈 저장
        size_bg_height = screen.get_size()[1]     #배경화면의 y사이즈 저장
        size_balloon_width = image_balloon.get_rect().size[0]  #풍선 가로 사이즈 저장
        size_balloon_height = image_balloon.get_rect().size[1]   #풍선 세로 사이즈 저장

        x_pos_balloon = random.randint(0, 700)   #x좌표 랜덤생성
        y_pos_balloon = random.randint(0, 300)  #y좌표 랜덤 생성
        x_speed_balloon = 1   #좌표들 (1,1)씩 증가
        y_speed_balloon = 1

        font = pygame.font.Font(None, 36)

        start_time = time.time()      #현재 시간을 start변수에 저장
        pause_time = 0             #pause_time = 0은 게임에서 일시 정지한 시간을 저장하는 변수 pause_time을 초기화하는 코드입니다.
        #이 변수는 게임에서 어떤 동작(예: 성공 메시지 표시 등)으로 인해 게임이 일시 정지될 때, 그 시간을 저장하는 데 사용됩니다. 
        is_paused = False  #게임이 일시정지 중인지 아닌지를 판단하는 함수입니다.

    while game_status == 'balloon_game':  # 플레이 하는 동안
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     
                game_run = False

            if event.type == pygame.MOUSEBUTTONDOWN:   #마우스 버튼 클릭 이벤트가 발생했을때
                if (
                    x_pos_balloon <= event.pos[0] <= x_pos_balloon + size_balloon_width
                    and y_pos_balloon <= event.pos[1] <= y_pos_balloon + size_balloon_height   #만약 x좌표가 풍선 사진의 왼쪽상단부터 풍선 사이즈를 더한만큼 사이에 있고 y좌표가 맨 왼쪽 위 y좌표부터 시작해 그 좌표 더하기 풍선 사이즈의 높이 만큼 더하면 그 사이에 마우스를 클릭하면 
                    ):
                    image_balloon = image_broken   # 풍선이 터진 풍선으로 이미지가 바뀌고
                    success_text = font.render("SUCCESS", True, (0, 255, 0))  #성공 문구가 뜬다.
                    screen.blit(success_text, (WIDTH // 2 - 180, HEIGHT // 2)) #배경화면 위에 성공 문구를 표시
                    pygame.display.update()  #그 문구 업데이트
                    pause_time = time.time() #현재 시간을 변수에 저장
                    is_paused = True   #잠시 pygame시간 정지
                    pygame.time.delay(2000)  # 2초 동안 일시 정지
                    is_paused = False    #다시 게임실행
                    score=score+1
                    game_status='main_game'
                else:   #마우스 버튼 클릭 이상한곳에다 하면
                    fail_text = font.render("FAIL", True, (255, 0, 0))     #실패문구
                    screen.blit(fail_text, (WIDTH // 2 - 130, HEIGHT // 2))  #실패 문구 출력
                    pygame.display.update()  #실패 문구 업데이트
                    time.sleep(2)   #프로그램을 2초동안 시간정지
                    game_status='main_game'

        if not is_paused:      #if not is_paused:은 파이썬의 조건문에서 사용되는 코드입니다. 이 코드는 is_paused 변수가 False일 때 조건이 참이 됩니다.not은 논리 부정 연산자로, 주어진 조건을 반전시킵니다. 따라서 if not is_paused:은 "만약 is_paused가 False라면"을 의미합니다. 즉, is_paused가 False일 때에만 해당 조건문의 코드 블록이 실행됩니다.
            elapsed_time = round(time.time() - start_time - pause_time, 2) #현재 시간에서 시작 시간을 빼고 일시정지 시간을 빼야 한다. 그걸 변수에 저장 일시정지 시간 안빼면 4초에 풍선을 클릭하면 success화면이2초동안 띄워져 있는데 그 사이에 fail문구가 뜬다.
        
        if elapsed_time > 6:  #경과 시간이 6초보다 크면
            fail_text = font.render("FAIL", True, (255, 0, 0))   #실패문구 출력
            screen.blit(fail_text, (WIDTH // 2 - 130, HEIGHT // 2))  #배경위에 실패문구 업데이트 
            pygame.display.update()  #파이게임 실패문구 업데이트
            time.sleep(2)  # 2초 동안 실패 메시지 표시
            game_status='main_game'

        x_pos_balloon += x_speed_balloon   #x좌표가 1씩 증가해서 풍선 위치를 1씩 옮김
        y_pos_balloon += y_speed_balloon

        if x_pos_balloon <= 0 or x_pos_balloon >= size_bg_width - size_balloon_width:   #만약 풍선의 x좌표가 화면을 벗어날려고 하면 위치 증가 변수를 음수로 바꿔서 방향을 튼다.
            x_speed_balloon = -x_speed_balloon

        if y_pos_balloon <= 0 or y_pos_balloon >= size_bg_height - size_balloon_height:
            y_speed_balloon = -y_speed_balloon

        screen.blit(image_bg, (0, 0))       #배경에 배경 이미지 업데이트
        screen.blit(image_balloon, (x_pos_balloon, y_pos_balloon)) #배경에 풍선 사진 랜덤으로 생성된 x좌표 y좌표에 업데이트
        pygame.display.update()    #사진들 파이게임에 업데이트


    # jump_game 진입
    # 플레이어 설정
    if game_status=='jump_game':
        player_width, player_height = 60, 60
        player_x, player_y = 0, 300
        player_speed = 5
        jump_height = 100
        jumping = False
        jump_count = 8  # 점프 속도를 빠르게 조정

    # 목적지 설정
        goal_size = 50
        goal_x, goal_y = WIDTH - goal_size - 20, HEIGHT - goal_size - 20

        # 블록 설정
        block_width, block_height = 60, 20
        block_gap = 100
        block_count = 5
        blocks = [(i * (block_width + block_gap) + 0, 350) for i in range(block_count)]  # 아래에 추가된 블록

         # 플레이어 이미지 설정
        player_image = pygame.image.load("image/man.png").convert_alpha()
        player_image = pygame.transform.scale(player_image, (player_width, player_height))

        # 배경 이미지 설정
        bg_image = pygame.image.load("image/house_bg.png")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

        # 시계 설정
        clock = pygame.time.Clock()

        # 시간 설정
        tmr = 5 * 60  # 5초

        # 폰트 설정
        font = pygame.font.Font(None, 36)

        # 추가: 게임 시작 시간 기록
        start_ticks = pygame.time.get_ticks()
        end_ticks = None

    while game_status=='jump_game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # left and right key
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # jump
        if not jumping:
            if keys[pygame.K_SPACE]:
                jumping = True
        else:
            if jump_count >= -8:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = 8

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        goal_rect = pygame.Rect(goal_x, goal_y, goal_size, goal_size)

        on_block = False
        for block in blocks:
            block_rect = pygame.Rect(block[0], block[1], block_width, block_height)
            if player_rect.colliderect(block_rect):
                on_block = True
                if not jumping:
                    player_y = block[1] - player_height

        # 배경 이미지 그리기
        screen.blit(bg_image, (0, 0))

        # 플레이어 이미지 그리기
        screen.blit(player_image, (player_x, player_y))

        # 목적지 그리기
        pygame.draw.rect(screen, (255, 0, 0), (goal_x, goal_y, goal_size, goal_size))

        # 블록 그리기
        for block in blocks:
            pygame.draw.rect(screen, (0, 0, 0), (block[0], block[1], block_width, block_height))

        # 시간 초과 and 낙사 and 성공
        tmr -= 1
        p_tmr = 0
        if tmr <= 0:
            tmr = 0
            game_status='main_game'
            if end_ticks is None:
                end_ticks = pygame.time.get_ticks()
        if player_y >= HEIGHT:
            if tmr <= 0:
                tmr = 0
                game_status='main_game'
            if end_ticks is None:
                end_ticks = pygame.time.get_ticks()

        if player_rect.colliderect(goal_rect):
            score = score+1
            game_status='main_game'

            if tmr <= 0:
                tmr = 0
            if end_ticks is None:
                end_ticks = pygame.time.get_ticks()

        # 아래로 떨어지기
        if not jumping and not on_block and player_y < HEIGHT - player_height:
            on_block_below = any( block[0] <= player_x <= block[0] + block_width and block[1] >= player_y + player_height for block in blocks )
            if not on_block_below:
                player_y += 5 # 아래로 이동

        # 공백에 착지해서 아래로 떨어져서 y가 스크린 맨 아래에 닿으면 종료
        if not on_block and player_y >= HEIGHT - player_height:
            game_status='main_game'
            if tmr <= 0:
                tmr = 0
            if end_ticks is None:
                end_ticks = pygame.time.get_ticks()
            
        # 시간 표시
        time_text = font.render(f"Time: {tmr // 60}", True, (0, 0, 0))
        screen.blit(time_text, (WIDTH - 150, 10))

        pygame.display.update()
        clock.tick(60)


    # death_screen
    if game_status == 'death_screen':
        game_font = pygame.font.Font(None, 60)
        score_board = game_font.render("score:"+str(int(score)), True, Black)

        hit = 0

        btn_main_death = Button("메인 화면", 400, 250, 140, 70, White, Blue, 36)

        while game_status == 'death_screen':
            screen.blit(score_board, (400, 200))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    btn_main_death.action(click_main)
                elif event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(FPS)

            pygame.display.update()


#########################################################################################################################################################################################################################################################################################################################################
############################################################################################################################################################################################ 메인 코드 작성, 미니게임 제작 및 수정, 코드 수정, 이미지 찾기, 이미지 제작,이미지 수정, 게임 아이디어 기획 = 'EASTERNLIGHT' ### 나는 힘들다 ######
#########################################################################################################################################################################################################################################################################################################################################

pygame.quit()