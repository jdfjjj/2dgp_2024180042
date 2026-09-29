from pico2d import *

open_canvas()

character = load_image('hero_spritesheet.png')

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas()
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas()
            exit()


frame = 0

for i in range(6 * 5):
    clear_canvas()
    character.clip_draw(frame * 80, 287, 80, 75, 400, 300, 400, 375)
    update_canvas()
    frame = (frame + 1) % 6
    delay(0.1)
    handle_events()

close_canvas()