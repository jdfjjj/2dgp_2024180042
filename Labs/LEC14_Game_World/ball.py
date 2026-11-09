from pico2d import get_canvas_width, load_image

import game_world

# 공의 객체를 정의

class Ball:
    image = None
                                            # 오른쪽이면 1, 왼쪽이면 -1
    def __init__(self, x, y, direction):    # 공의 시작 좌표(x,y) / 방향(direction) 설정.
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.direction = direction

    def update(self):           # 공의 좌표를 업데이트하고, 화면 밖으로 나가면 게임월드에서 제거
        self.x += self.direction * 10   # 공의 이동 속도는 10픽셀/프레임. 한번 실행될 때마다 공의 가로 위치를 direction *10만큼 바꿈
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)  # 공이 화면의 오른쪽이나 왼쪽을 벗어나면 이 코드로 월드에서 제거

    def draw(self):
        Ball.image.draw(self.x, self.y)
