import math

import pygame

from enum import Enum

from src.utils import easyTween, particles
from src.utils.drawing import rendering, drawing


class SwordState(Enum):
    AIM = 0
    SWING = 1
class Sword(pygame.sprite.Sprite):
    def __init__(self, game, parent):
        super().__init__()
        self.game = game
        self.parent = parent

        self.state = SwordState.AIM
        self.swing_time = 0.1
        self.target_angle = 0
        self.dir = 1
        self.image = drawing.load_asset("images/weapons/sword.png")
        self.image = pygame.transform.rotate(self.image, -90)
        self.sword_offset = 0

        self.swing_tween = None
        self.swing_timer = None

    def swing(self):
        if self.state == SwordState.AIM:
            self.state = SwordState.SWING
            self.swing_tween = easyTween.Tween(self, "dir", self.dir, -self.dir, self.swing_time)
            self.swing_timer = easyTween.Timer(self, self.swing_time * 0.5, func_name="spawn_swing_particle")

    def update(self, dt, target_pos):
        screen_pos = self.game.camera.to_screen((self.parent.centerx, self.parent.centery))
        self.target_angle = -math.degrees(math.atan2(target_pos[1] - screen_pos[1], target_pos[0] - screen_pos[0]))
        match self.state:
            case SwordState.AIM:
                pass
            case SwordState.SWING:
                if self.swing_tween.done:
                    self.swing_tween = None
                    self.state = SwordState.AIM

    def draw(self, renderer):
        offset_angle = self.target_angle - 90 * self.dir
        swing_angle = self.target_angle - 180 * self.dir

        screenx, screeny = self.game.camera.to_screen((self.parent.centerx, self.parent.centery))

        screenx += math.cos(math.radians(offset_angle)) * self.sword_offset
        screeny -= math.sin(math.radians(offset_angle)) *  self.sword_offset

        screenx += math.cos(math.radians(swing_angle)) * self.image.get_width() * 0.5
        screeny -= math.sin(math.radians(swing_angle)) * self.image.get_width() * 0.5

        renderer.submit(rendering.DrawCmd(20, "smooth", self.image, (screenx, screeny), angle_deg=swing_angle))

    def spawn_swing_particle(self):
        particles.Particle(self.parent.centerx, self.parent.centery, (5, 5), 300, -self.target_angle,
                           (200, 200, 200, 200), accel=-900, lifetime=0.35)
