# 실습 과제 진행
from pico2d import *
import math

# 맨처음 해야할 일
open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    print('CIRCLE')
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        # 캐릭터 이미지 표시
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    pass 

def draw_top():
    print('TOP')
    pass

def draw_right():
    print('RIGHT')
    pass

def draw_bottom():
    print('BOTTOM')
    pass

def draw_left():
    print('LEFT')
    pass


def move_rectangle():
    print('RECTANGLE')
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    pass

def move_triangle():
    print('TRIANGLE')
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()

