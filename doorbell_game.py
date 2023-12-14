import pygame
import sys
import random

pygame.init()

pygame.display.set_caption("초인종 누르기")
screen=pygame.display.set_mode((800,400))

Clock=pygame.time.Clock()
total_time=5
start_tick=pygame.time.get_ticks()

bg = pygame.image.load("image/door.png")
up_image = pygame.image.load("image/up.png")
down_image = pygame.image.load("image/down.png")
left_image = pygame.image.load("image/left.png")
right_image = pygame.image.load("image/right.png")

up=pygame.K_UP
down=pygame.K_DOWN
left=pygame.K_LEFT
right=pygame.K_RIGHT

bell_type = [up, down, left, right]
bell = random.choice(bell_type)

arrow_image = None
if bell == up:
    arrow_image = up_image
if bell == down:
    arrow_image = down_image
if bell == left:
    arrow_image = left_image
if bell == right:
    arrow_image = right_image

count=0
running=True
pygame.display.update()
while running:
    t=Clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if count==5:
            count=0
            print("성공")
            arrow_image=None
            bell=None
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==bell:
                count=count+1

    screen.blit(bg,(0,0))
    screen.blit(arrow_image,(325,110))
    pygame.display.update()
    
    game_font = pygame.font.Font(None, 40)
    run_time=(pygame.time.get_ticks()-start_tick)/1000
    timer=game_font.render("timer:" + str(int(total_time - run_time)),True,(255,255,255))
    screen.blit(timer,(10,10))
    
    pygame.display.update()

    if (total_time-run_time) <= 0:
        print("GAME OVER")
        running=False

pygame.quit()