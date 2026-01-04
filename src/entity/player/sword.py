import math

import pygame

from enum import Enum

from src.utils import easyTween
from src.utils.drawing import rendering


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
        self.image = pygame.surface.Surface((40, 8), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 100, 20))
        self.sword_offset = 0

        self.swing_tween = None

    def swing(self):
        if self.state == SwordState.AIM:
            self.state = SwordState.SWING
            self.swing_tween = easyTween.Tween(self, "dir", self.dir, -self.dir, self.swing_time)

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

        rotated = pygame.transform.rotate(self.image, swing_angle)
        rotated_rect = rotated.get_rect()
        screenx, screeny = self.game.camera.to_screen((self.parent.centerx - rotated_rect.w * 0.5, self.parent.centery - rotated_rect.h * 0.5))

        screenx += math.cos(math.radians(offset_angle)) * self.sword_offset
        screeny -= math.sin(math.radians(offset_angle)) *  self.sword_offset

        screenx += math.cos(math.radians(swing_angle)) * self.image.get_width() * 0.5
        screeny -= math.sin(math.radians(swing_angle)) * self.image.get_width() * 0.5

        renderer.submit(rendering.DrawCmd(20, "smooth", rotated, (screenx, screeny)))