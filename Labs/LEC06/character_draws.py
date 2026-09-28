# 실습 과제 진행
from pico2d import *
import math

# 맨처음 해야할 일
open_canvas(800, 600)

character = load_image('character.png')


def draw_circle():
    print('CIRCLE')
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        # 캐릭터 이미지 표시
        draw_character(x, y)
    pass

def draw_top():
    print('TOP')
    for x in range(50, 751, 5):
       draw_character(x, 550)
    pass

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)
    pass

def draw_right():
    print('RIGHT')
    for y in range(550, 49, -5):
        draw_character(750, y)
    pass

def draw_bottom():
    print('BOTTOM')
    for x in range(750, 49, -5):
        draw_character(x, 50)
    pass

def draw_left():
    print('LEFT')
    for y in range(50, 551, 5):
        draw_character(50, y)
    pass


def draw_rectangle():
    print('RECTANGLE')
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass

def draw_ab():
    print('AB')
    x0, y0 = 100, 100
    x1, y1 = 700, 100
    n = 100
    for step in range(n + 1):
        t = step / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        draw_character(x, y)
    pass

def draw_bc():
    print('BC')
    pass

def draw_ca():
    print('CA')
    pass

def draw_triangle():
    print('TRIANGLE')
    draw_ab()
    draw_bc()
    draw_ca()
    pass

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    pass

close_canvas()

