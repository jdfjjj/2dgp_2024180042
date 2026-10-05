from dataclasses import dataclass
import sys
from pathlib import Path
from time import perf_counter

from pico2d import *


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
POLL_INTERVAL = 0.01
FRAME_INTERVAL = 0.08
REPEAT_COUNT = 5
ACTION_PAUSE = 1.0
SHEET_WIDTH = 399
SHEET_HEIGHT = 525
FRAME_SCALE = 8
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class Frame:
    left: int
    top: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]


def frame_sequence(*rectangles: tuple[int, int, int, int]) -> tuple[Frame, ...]:
    return tuple(Frame(*rectangle) for rectangle in rectangles)


# Rectangles use image coordinates from the top-left and follow visible alpha bounds.
ANIMATIONS = (
    Animation("동작 01", frame_sequence(
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
        (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 39),
        (270, 45, 24, 32), (302, 51, 29, 26),
    )),
    Animation("동작 02", frame_sequence(
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 37),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 79, 24, 38), (263, 79, 30, 38),
        (295, 79, 36, 38), (334, 80, 32, 35), (370, 79, 29, 38),
    )),
    Animation("동작 03", frame_sequence(
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    )),
    Animation("동작 04", frame_sequence(
        (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 168, 31, 30), (268, 170, 30, 30),
    )),
    Animation("동작 05", frame_sequence(
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    )),
    Animation("동작 06", frame_sequence(
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    )),
    Animation("동작 07", frame_sequence(
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    )),
    Animation("동작 08", frame_sequence(
        (1, 326, 24, 45), (31, 327, 29, 43), (65, 327, 20, 43),
        (90, 327, 25, 42), (119, 327, 24, 42), (149, 327, 20, 43),
    )),
    Animation("동작 09", frame_sequence(
        (184, 341, 40, 27), (232, 341, 39, 27),
    )),
    Animation("동작 10", frame_sequence(
        (1, 379, 27, 37), (31, 379, 31, 35), (64, 379, 31, 35),
        (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 35), (254, 378, 33, 36),
    )),
    Animation("동작 11", frame_sequence(
        (6, 429, 34, 40), (49, 426, 34, 43),
        (96, 427, 23, 39), (125, 427, 23, 39),
    )),
)


class AnimationPlayer:
    def __init__(
        self,
        animations: tuple[Animation, ...],
        start_time: float,
    ) -> None:
        if not animations or any(not animation.frames for animation in animations):
            raise ValueError("재생 목록과 각 동작에는 프레임이 하나 이상 필요합니다.")

        self.animations = animations
        self.animation_index = 0
        self.frame_index = 0
        self.completed_repeats = 0
        self.next_frame_at = start_time + FRAME_INTERVAL
        self.wait_until: float | None = None

    @property
    def current_animation(self) -> Animation:
        return self.animations[self.animation_index]

    @property
    def current_frame(self) -> Frame:
        return self.current_animation.frames[self.frame_index]

    def update(self, now: float) -> None:
        if self.wait_until is not None or now < self.next_frame_at:
            return

        self.next_frame_at = now + FRAME_INTERVAL
        self.frame_index = (self.frame_index + 1) % len(self.current_animation.frames)


def handle_events() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def draw_frame(sprite, frame: Frame) -> None:
    source_bottom = SHEET_HEIGHT - frame.top - frame.height
    sprite.clip_draw(
        frame.left,
        source_bottom,
        frame.width,
        frame.height,
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        frame.width * FRAME_SCALE,
        frame.height * FRAME_SCALE,
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
            draw_frame(sprite, ANIMATIONS[0].frames[0])
            update_canvas()
            delay(POLL_INTERVAL)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
