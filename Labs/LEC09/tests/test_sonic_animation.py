import io
import importlib.util
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch


_pico2d_stub = types.ModuleType("pico2d")
_pico2d_stub.SDL_QUIT = 1
for _name in (
    "open_canvas",
    "load_image",
    "get_events",
    "clear_canvas",
    "update_canvas",
    "delay",
    "close_canvas",
):
    setattr(_pico2d_stub, _name, lambda *arguments: None)
sys.modules.setdefault("pico2d", _pico2d_stub)

_source = Path(__file__).resolve().parents[1] / "sonic_animation.py"
_spec = importlib.util.spec_from_file_location("sonic_animation_under_test", _source)
assert _spec is not None and _spec.loader is not None
sonic_animation = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = sonic_animation
_spec.loader.exec_module(sonic_animation)


class PlaybackTests(unittest.TestCase):
    def setUp(self) -> None:
        frames = sonic_animation.ANIMATIONS[0].frames[:2]
        animation = sonic_animation.Animation("시험 동작", frames)
        self.player = sonic_animation.AnimationPlayer((animation,), 0.0)

    def test_action_repeats_five_complete_frame_cycles(self) -> None:
        for _ in range(2 * (sonic_animation.REPEAT_COUNT - 1)):
            self.player.update(self.player.next_frame_at)

        self.assertEqual(self.player.completed_repeats, 4)
        self.assertIsNone(self.player.wait_until)

        for _ in range(2):
            self.player.update(self.player.next_frame_at)

        self.assertEqual(self.player.completed_repeats, 5)
        self.assertIsNotNone(self.player.wait_until)
        self.assertEqual(self.player.frame_index, 1)

    def test_frame_changes_only_after_its_interval(self) -> None:
        first_frame = self.player.current_frame
        self.player.update(self.player.next_frame_at - 0.001)
        self.assertEqual(self.player.current_frame, first_frame)

        self.player.update(self.player.next_frame_at)
        self.assertEqual(self.player.frame_index, 1)

    def test_wait_then_advances_and_wraps_to_first_action(self) -> None:
        frames = sonic_animation.ANIMATIONS[0].frames[:2]
        animations = (
            sonic_animation.Animation("첫째", frames),
            sonic_animation.Animation("둘째", frames),
        )
        player = sonic_animation.AnimationPlayer(animations, 0.0)

        for _ in range(2 * sonic_animation.REPEAT_COUNT):
            player.update(player.next_frame_at)
        wait_end = player.wait_until
        self.assertIsNotNone(wait_end)
        self.assertEqual(wait_end, player.next_frame_at - sonic_animation.FRAME_INTERVAL + 1.0)

        player.update(wait_end - 0.001)
        self.assertEqual(player.animation_index, 0)
        player.update(wait_end)
        self.assertEqual(player.animation_index, 1)
        self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.completed_repeats, 0)

        for _ in range(2 * sonic_animation.REPEAT_COUNT):
            player.update(player.next_frame_at)
        player.update(player.wait_until)
        self.assertEqual(player.animation_index, 0)


class FrameDataTests(unittest.TestCase):
    def test_all_animation_frames_stay_within_the_sprite_sheet(self) -> None:
        self.assertEqual(len(sonic_animation.ANIMATIONS), 11)
        self.assertEqual(sum(len(item.frames) for item in sonic_animation.ANIMATIONS), 76)
        for animation in sonic_animation.ANIMATIONS:
            for frame in animation.frames:
                with self.subTest(animation=animation.name, frame=frame):
                    self.assertGreaterEqual(frame.left, 0)
                    self.assertGreaterEqual(frame.top, 0)
                    self.assertGreater(frame.width, 0)
                    self.assertGreater(frame.height, 0)
                    self.assertLessEqual(frame.left + frame.width, sonic_animation.SHEET_WIDTH)
                    self.assertLessEqual(frame.top + frame.height, sonic_animation.SHEET_HEIGHT)

    def test_draw_frame_converts_top_origin_and_preserves_scale_ratio(self) -> None:
        class Image:
            arguments = None

            def clip_draw(self, *arguments):
                self.arguments = arguments

        image = Image()
        frame = sonic_animation.Frame(8, 80, 26, 37)
        sonic_animation.draw_frame(image, frame, 500)

        self.assertEqual(
            image.arguments,
            (8, 408, 26, 37, 500, 400, 26 * 12, 37 * 12),
        )
        self.assertEqual(image.arguments[6] / image.arguments[7], 26 / 37)


class WindowLifecycleTests(unittest.TestCase):
    def test_missing_sprite_reports_error_before_opening_window(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing_sprite = Path(directory) / "missing.png"
            error_output = io.StringIO()
            with (
                patch.object(sonic_animation, "SPRITE_PATH", missing_sprite),
                patch.object(sonic_animation, "open_canvas") as open_canvas,
                redirect_stderr(error_output),
            ):
                sonic_animation.main()

        open_canvas.assert_not_called()
        self.assertIn("스프라이트 시트를 찾을 수 없습니다", error_output.getvalue())

    def test_window_close_event_releases_canvas(self) -> None:
        class Image:
            def clip_draw(self, *arguments):
                pass

        event_batches = [[], [types.SimpleNamespace(type=sonic_animation.SDL_QUIT)]]
        with (
            patch.object(sonic_animation, "open_canvas") as open_canvas,
            patch.object(sonic_animation, "load_image", return_value=Image()),
            patch.object(sonic_animation, "get_events", side_effect=event_batches),
            patch.object(sonic_animation, "clear_canvas"),
            patch.object(sonic_animation, "update_canvas"),
            patch.object(sonic_animation, "delay"),
            patch.object(sonic_animation, "close_canvas") as close_canvas,
        ):
            sonic_animation.main()

        open_canvas.assert_called_once_with(1200, 800)
        close_canvas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
