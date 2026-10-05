import importlib.util
import sys
import types
import unittest
from pathlib import Path


_pico2d_stub = types.ModuleType("pico2d")
_pico2d_stub.SDL_QUIT = 1
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


if __name__ == "__main__":
    unittest.main()
