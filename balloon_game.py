import pygame  #파이게임 모듈추가
import random   #랜덤모듈 추가 (풍선게임 실행할때마다 위치 무작위 생성)
import time    # 시간 관련 모듈 추가 (5초 안에 풍선을 터뜨려야 하기 때문에 )
import sys     #sys.exit()를 호출하여 파이썬 프로그램 전체를 종료합니다.

clock=pygame.time.Clock()
FPS=60

pygame.init()   #파이게임 초기화
width, height = 800, 400  #가로 800,세로 400 픽셀
background = pygame.display.set_mode((width, height))  #배경화면 크기
pygame.display.set_caption("Pop the Balloon Game")   #게임 제목

image_bg = pygame.image.load("image/house_bg.png")    # 이미지 변수 대입
image_balloon = pygame.image.load("image/balloon.png")
image_broken = pygame.image.load("image/pop.png")

size_bg_width = background.get_size()[0]     #배경화면의 x사이즈 저장
size_bg_height = background.get_size()[1]     #배경화면의 y사이즈 저장
size_balloon_width = image_balloon.get_rect().size[0]  #풍선 가로 사이즈 저장
size_balloon_height = image_balloon.get_rect().size[1]   #풍선 세로 사이즈 저장

x_pos_balloon = random.randint(0, 700)   #x좌표 랜덤생성
y_pos_balloon = random.randint(0, 300)  #y좌표 랜덤 생성
x_speed_balloon = 1   #좌표들 (1,1)씩 증가
y_speed_balloon = 1

font = pygame.font.Font(None, 36)

play = True
start_time = time.time()      #현재 시간을 start변수에 저장
pause_time = 0             #pause_time = 0은 게임에서 일시 정지한 시간을 저장하는 변수 pause_time을 초기화하는 코드입니다.
#이 변수는 게임에서 어떤 동작(예: 성공 메시지 표시 등)으로 인해 게임이 일시 정지될 때, 그 시간을 저장하는 데 사용됩니다. 
is_paused = False  #게임이 일시정지 중인지 아닌지를 판단하는 함수입니다.
success_count = 0  # 게임 성공하면 +1씩 증가할 변수
game_failed = 0    # 게임 실패 횟수를 저장하는 변수

while play:    # 플레이 하는 동안
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     
            play = False

        if event.type == pygame.MOUSEBUTTONDOWN:   #마우스 버튼 클릭 이벤트가 발생했을때
            if (
                x_pos_balloon <= event.pos[0] <= x_pos_balloon + size_balloon_width
                and y_pos_balloon <= event.pos[1] <= y_pos_balloon + size_balloon_height   #만약 x좌표가 풍선 사진의 왼쪽상단부터 풍선 사이즈를 더한만큼 사이에 있고 y좌표가 맨 왼쪽 위 y좌표부터 시작해 그 좌표 더하기 풍선 사이즈의 높이 만큼 더하면 그 사이에 마우스를 클릭하면 
            ):
                image_balloon = image_broken   # 풍선이 터진 풍선으로 이미지가 바뀌고
                success_text = font.render("SUCCESS", True, (0, 255, 0))  #성공 문구가 뜬다.
                background.blit(success_text, (width // 2 - 180, height // 2)) #배경화면 위에 성공 문구를 표시
                pygame.display.update()  #그 문구 업데이트
                pause_time = time.time() #현재 시간을 변수에 저장
                is_paused = True   #잠시 pygame시간 정지
                pygame.time.delay(2000)  # 2초 동안 일시 정지
                is_paused = False    #다시 게임실행
                success_count += 1  # 성공시 포인트 1점 증가 
                play = False    #화면 닫음
            else:   #마우스 버튼 클릭 이상한곳에다 하면
                fail_text = font.render("FAIL", True, (255, 0, 0))     #실패문구
                background.blit(fail_text, (width // 2 - 130, height // 2))  #실패 문구 출력
                pygame.display.update()  #실패 문구 업데이트
                time.sleep(2)   #프로그램을 2초동안 시간정지
                game_failed += 1  # 실패 횟수 증가 
                play = False  #게임 꺼짐

    if not is_paused:      #if not is_paused:은 파이썬의 조건문에서 사용되는 코드입니다. 이 코드는 is_paused 변수가 False일 때 조건이 참이 됩니다.not은 논리 부정 연산자로, 주어진 조건을 반전시킵니다. 따라서 if not is_paused:은 "만약 is_paused가 False라면"을 의미합니다. 즉, is_paused가 False일 때에만 해당 조건문의 코드 블록이 실행됩니다.
        elapsed_time = round(time.time() - start_time - pause_time, 2) #현재 시간에서 시작 시간을 빼고 일시정지 시간을 빼야 한다. 그걸 변수에 저장 일시정지 시간 안빼면 4초에 풍선을 클릭하면 success화면이2초동안 띄워져 있는데 그 사이에 fail문구가 뜬다.
        
        if elapsed_time > 6:  #경과 시간이 6초보다 크면
            fail_text = font.render("FAIL", True, (255, 0, 0))   #실패문구 출력
            background.blit(fail_text, (width // 2 - 130, height // 2))  #배경위에 실패문구 업데이트 
            pygame.display.update()  #파이게임 실패문구 업데이트
            time.sleep(2)  # 2초 동안 실패 메시지 표시
            game_failed += 1  # 실패 횟수 증가
            play = False   #게임 종료

        x_pos_balloon += x_speed_balloon   #x좌표가 1씩 증가해서 풍선 위치를 1씩 옮김
        y_pos_balloon += y_speed_balloon

        if x_pos_balloon <= 0 or x_pos_balloon >= size_bg_width - size_balloon_width:             #만약 풍선의 x좌표가 화면을 벗어날려고 하면 위치 증가 변수를 음수로 바꿔서 방향을 튼다.
            x_speed_balloon = -x_speed_balloon

        if y_pos_balloon <= 0 or y_pos_balloon >= size_bg_height - size_balloon_height:
            y_speed_balloon = -y_speed_balloon

        background.blit(image_bg, (0, 0))       #배경에 배경 이미지 업데이트
        background.blit(image_balloon, (x_pos_balloon, y_pos_balloon)) #배경에 풍선 사진 랜덤으로 생성된 x좌표 y좌표에 업데이트
        pygame.display.update()    #사진들 파이게임에 업데이트

# 게임 종료 후 성공한 풍선의 개수와 실패 횟수 출력
print(f"성공 풍선게임에 변수 1추가: {success_count}")     
print(f"미니게임 실패 횟수: {game_failed}")

pygame.quit()
sys.exit()