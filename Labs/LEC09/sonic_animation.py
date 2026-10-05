import sys
from pathlib import Path

from pico2d import *


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
POLL_INTERVAL = 0.01
SHEET_WIDTH = 399
SHEET_HEIGHT = 525
FRAME_SCALE = 8
PREVIEW_FRAME = (1, 39, 29, 39)
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


def handle_events() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def draw_frame(sprite, frame: tuple[int, int, int, int]) -> None:
    left, top, width, height = frame
    source_bottom = SHEET_HEIGHT - top - height
    sprite.clip_draw(
        left,
        source_bottom,
        width,
        height,
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        width * FRAME_SCALE,
        height * FRAME_SCALE,
    )


def main() -> None:
    if not SPRITE_PATH.is_file():
        print(f"오류: 스프라이트 시트를 찾을 수 없습니다: {SPRITE_PATH}", file=sys.stderr)
        return

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        sprite = load_image(str(SPRITE_PATH))
        running = True
        while running:
            running = handle_events()
            clear_canvas()
            draw_frame(sprite, PREVIEW_FRAME)
            update_canvas()
            delay(POLL_INTERVAL)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
