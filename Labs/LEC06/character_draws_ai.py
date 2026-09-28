from pico2d import *
import math

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CENTER_X = 400
CENTER_Y = 300
CIRCLE_RADIUS = 200
RECT_LEFT = 50
RECT_RIGHT = 750
RECT_BOTTOM = 50
RECT_TOP = 550

character = None


def initialize():
	global character
	open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
	character = load_image('character.png')


def draw_character(x, y):
	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(0.01)
	get_events()


def circle_position(angle):
	radians = math.radians(angle)
	x = CENTER_X + CIRCLE_RADIUS * math.cos(radians)
	y = CENTER_Y + CIRCLE_RADIUS * math.sin(radians)
	return x, y


def draw_circle():
	for angle in range(360):
		x, y = circle_position(angle)
		draw_character(x, y)


def draw_top():
	for x in range(RECT_LEFT, RECT_RIGHT + 1, 5):
		draw_character(x, RECT_TOP)


def draw_right():
	for y in range(RECT_TOP, RECT_BOTTOM - 1, -5):
		draw_character(RECT_RIGHT, y)


def draw_bottom():
	for x in range(RECT_RIGHT, RECT_LEFT - 1, -5):
		draw_character(x, RECT_BOTTOM)
