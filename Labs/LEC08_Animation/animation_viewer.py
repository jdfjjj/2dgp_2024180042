from pico2d import *

open_canvas()

character = load_image('hero_spritesheet.png')

walk_frames = [(i * 80, 287, 80, 75) for i in range(6)]
run_frames = [(i * 80, 194, 80, 75) for i in range(6)]
jump_frames = [(i * 80, 107, 80, 75) for i in range(3)]
death_frames = [(left, 107, 85, 75) for left in (258, 327, 412, 503)]

jump_heights = [0, 80, 120]   

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas()
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas()
            exit()

def draw_frame(frames, frame, y):
    left, bottom, width, height = frames[frame]
    clear_canvas()
    character.clip_draw(left, bottom, width, height, 400, y, width * 5, height * 5)
    update_canvas()

def play_animation(frames, frame_delay, heights=None):
    frame = 0
    for i in range(len(frames) * 5):
        y = 300
        if heights:
            y = 300 + heights[frame]
        draw_frame(frames, frame, y)
        frame = (frame + 1) % len(frames)
        delay(frame_delay)
        handle_events()
    if heights:
        draw_frame(frames, 0, 300)  
    delay(1.0)

while True:
    play_animation(walk_frames, 0.1)                   # 걷기
    play_animation(run_frames, 0.06)                   # 뛰기
    play_animation(jump_frames, 0.15, jump_heights)    # 점프
    play_animation(death_frames, 0.2)                  # 죽음