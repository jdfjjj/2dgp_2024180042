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
