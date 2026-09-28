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

def move_right():
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
    draw_left()
    draw_bottom()
    draw_right()
    pass

def draw_triangle():
    print('TRIANGLE')
    pass

while True:
    # draw_circle()
    draw_rectangle()
    draw_triangle()
    pass

close_canvas()

