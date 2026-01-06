from dataclasses import dataclass

import pygame

@dataclass
class AnimInfo:
    name: str
    frames: int
    fps: int
    loop: bool = False
    ping_pong: bool = False

class SpriteSheet:
    def __init__(self, spritesheet, frame_w, frame_h):
        self.spritesheet = spritesheet.convert_alpha()
        self.frame_w = frame_w
        self.frame_h = frame_h
        self._frame_cache = {}  # (col,row) -> Surface

    def get_frame(self, col, row, flip_x, flip_y):
        key = (col, row, flip_x, flip_y)
        if key in self._frame_cache:
            return self._frame_cache[key]

        rect = pygame.Rect(col * self.frame_w, row * self.frame_h, self.frame_w, self.frame_h)
        frame = pygame.Surface((self.frame_w, self.frame_h), pygame.SRCALPHA)
        frame.blit(self.spritesheet, (0, 0), rect)
        if flip_x or flip_y:
            frame = pygame.transform.flip(frame, flip_x, flip_y)

        self._frame_cache[key] = frame
        return frame

class SpriteSheetAnimation:
    def __init__(self, name, spritesheet: SpriteSheet, row, frames, fps=12, loop=False, ping_pong=False):
        self.name = name
        self._spritesheet = spritesheet
        self._row = row
        self._frames = frames
        self._loop = loop
        self._ping_pong = ping_pong

        self._frame_time = 1.0 / fps
        self._time_acc = 0.0

        self._frame_index = 0
        self.flip_x = False
        self.flip_y = False
        self._done = False
        self._time_acc_dir = 1


    def reset(self):
        self._time_acc = 0.0
        self._frame_index = 0
        self._done = False
        self._time_acc_dir = 1

    def update(self, dt: float):
        if self._done or self._frames <= 1:
            return

        self._time_acc += dt
        steps = int(self._time_acc / self._frame_time)
        if steps <= 0:
            return
        self._time_acc -= steps * self._frame_time

        for _ in range(steps):
            self._frame_index += self._time_acc_dir

            if not self._ping_pong:
                # ---- normal forward playback ----
                if self._frame_index >= self._frames:
                    if self._loop:
                        self._frame_index = 0
                    else:
                        self._frame_index = self._frames - 1
                        self._done = True
                        return

            else:
                # ---- ping-pong playback ----
                if self._time_acc_dir == 1 and self._frame_index >= self._frames:
                    # went past the end: bounce
                    self._time_acc_dir = -1
                    self._frame_index = self._frames - 2  # bounce to the frame before last (avoid repeating last)

                elif self._time_acc_dir == -1 and self._frame_index < 0:
                    # went past the start
                    if self._loop:
                        # bounce and keep going forever
                        self._time_acc_dir = 1
                        self._frame_index = 1  # avoid repeating frame 0
                    else:
                        # finish after one back-and-forth
                        self._frame_index = 0
                        self._done = True
                        return

    @property
    def image(self):
        return self._spritesheet.get_frame(self._frame_index, self._row, self.flip_x, self.flip_y)


class AnimationManager:
    def __init__(self, spritesheet: SpriteSheet, anim_info: list[AnimInfo]):
        self.spritesheet = spritesheet
        self.animations = {}
        for i in range(len(anim_info)):
            info = anim_info[i]
            self.animations[info.name] = SpriteSheetAnimation(
                name=info.name,
                spritesheet=spritesheet,
                row=i,
                frames=info.frames,
                fps=info.fps,
                loop=info.loop,
                ping_pong=info.ping_pong
            )

        self.cur_anim_name = anim_info[0].name

        keys = list(self.animations)
        for name in keys:
            print(self.animations[name])

    @property
    def cur_anim(self):
        return self.animations[self.cur_anim_name]

    def set_anim(self, anim_name):
        if self.cur_anim_name == anim_name:
            return

        self.cur_anim_name = anim_name
        self.cur_anim.reset()

    def update(self, dt):
        self.cur_anim.update(dt)
