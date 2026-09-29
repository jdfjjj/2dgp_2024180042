from pico2d import *

open_canvas()

character = load_image('hero_spritesheet.png')

frame = 0

for i in range(6):
    clear_canvas()
    character.clip_draw(frame * 80, 287, 80, 75, 400, 300, 400, 375)
    update_canvas()
    frame = frame + 1
    delay(0.1)

close_canvas()