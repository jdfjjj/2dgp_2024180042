import sys
from pathlib import Path

from pico2d import *


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
POLL_INTERVAL = 0.01
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


def handle_events() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def main() -> None:
    if not SPRITE_PATH.is_file():
        print(f"오류: 스프라이트 시트를 찾을 수 없습니다: {SPRITE_PATH}", file=sys.stderr)
        return

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        running = True
        while running:
            running = handle_events()
            clear_canvas()
            update_canvas()
            delay(POLL_INTERVAL)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
