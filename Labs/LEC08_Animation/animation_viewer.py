from pico2d import *

open_canvas()

character = load_image('hero_spritesheet.png')

clear_canvas()
character.clip_draw(0, 287, 80, 75, 400, 300, 400, 375)
update_canvas()
delay(2)

close_canvas()