from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

RUN_LEFT, RUN_RIGHT, IDLE_LEFT, IDLE_RIGHT = 0, 1, 2, 3
SPEED = 10
MARGIN_X = 25
MARGIN_Y = 50


def handle_events():
    global running
    global dir_x, dir_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


def update_character():
    global x, y, facing

    if dir_x > 0:
        facing = 1
    elif dir_x < 0:
        facing = -1

    x += dir_x * SPEED
    y += dir_y * SPEED

    x = clamp(MARGIN_X, x, TUK_WIDTH - MARGIN_X)
    y = clamp(MARGIN_Y, y, TUK_HEIGHT - MARGIN_Y)


def get_action():
    if dir_x == 0 and dir_y == 0:
        return IDLE_RIGHT if facing == 1 else IDLE_LEFT
    return RUN_RIGHT if facing == 1 else RUN_LEFT


running = True
frame = 0
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
dir_x, dir_y = 0, 0
facing = 1

while running:
    clear_canvas()

    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * get_action(), 100, 100, x, y)

    update_canvas()
    handle_events()
    update_character()
    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()