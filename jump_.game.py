import pygame
from pygame.locals import *
import sys

# 초기화
pygame.init()


# 화면 설정
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump Map")

# 플레이어 설정
player_width, player_height = 60, 60
player_x, player_y = 0, 300
player_speed = 5
jump_height = 100
jumping = False
jump_count = 8  # 점프 속도를 빠르게 조정

# 목적지 설정
goal_size = 50
goal_x, goal_y = screen_width - goal_size - 20, screen_height - goal_size - 20

# 블록 설정
block_width, block_height = 60, 20
block_gap = 100
block_count = 5
blocks = [(i * (block_width + block_gap) + 0, 350)
          for i in range(block_count)]  # 아래에 추가된 블록

# 플레이어 이미지 설정
player_image = pygame.image.load("image/man.png").convert_alpha()
player_image = pygame.transform.scale(
    player_image, (player_width, player_height))

# 배경 이미지 설정
bg_image = pygame.image.load("image/house_bg.png")
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

# 시계 설정
clock = pygame.time.Clock()

# 시간 설정
tmr = 5 * 60  # 5초

# 폰트 설정
font = pygame.font.Font(None, 36)

# 추가: 게임 결과 변수
Suc = 0
Fail = 0

# 추가: 게임 시작 시간 기록
start_ticks = pygame.time.get_ticks()
end_ticks = None

# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # left and right key
    if keys[K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # jump
    if not jumping:
        if keys[K_SPACE]:
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
    pygame.draw.rect(screen, (255, 0, 0),
                     (goal_x, goal_y, goal_size, goal_size))

    # 블록 그리기
    for block in blocks:
        pygame.draw.rect(screen, (0, 0, 0),
                         (block[0], block[1], block_width, block_height))

    # 시간 초과 and 낙사 and 성공
    tmr -= 1
    p_tmr = 0
    if tmr <= 0:
        tmr = 0
        Fail = 1
        if end_ticks is None:
            end_ticks = pygame.time.get_ticks()
    if player_y >= screen_height:
        if tmr <= 0:
            tmr = 0
        Fail = 1
        if end_ticks is None:
            end_ticks = pygame.time.get_ticks()

    if player_rect.colliderect(goal_rect):
        Suc = 1

        if tmr <= 0:
            tmr = 0
        if end_ticks is None:
            end_ticks = pygame.time.get_ticks()

    # 아래로 떨어지기
    if not jumping and not on_block and player_y < screen_height - player_height:
        on_block_below = any(
            block[0] <= player_x <= block[0] +
            block_width and block[1] >= player_y + player_height
            for block in blocks
        )
        if not on_block_below:
            player_y += 5  # 아래로 이동

    # 공백에 착지해서 아래로 떨어져서 y가 스크린 맨 아래에 닿으면 종료
    if not on_block and player_y >= screen_height - player_height:
        Fail = 1
        if tmr <= 0:
            tmr = 0
            Fail = 1
        if end_ticks is None:
            end_ticks = pygame.time.get_ticks()

    # 게임 클리어 또는 실패 시 메시지 출력
    if Suc == 1 or Fail == 1:
        # 두 가지 상황에 대한 메시지 출력
        if Suc == 1:
            message = font.render("SUCCESS", True, (0, 0, 255))
        else:
            message = font.render("FAIL", True, (255, 0, 0))

        # 메시지를 화면 중앙에 위치시키기
        message_rect = message.get_rect(
            center=(screen_width // 2, screen_height // 2))
        screen.blit(message, message_rect)

        # 2초 대기 후 게임 종료
        if pygame.time.get_ticks() - end_ticks >= 2000:
            pygame.quit()
            sys.exit()

    # 시간 표시
    time_text = font.render(f"Time: {tmr // 60}", True, (0, 0, 0))
    screen.blit(time_text, (screen_width - 150, 10))

    pygame.display.update()
    clock.tick(60)

