import math
from typing import Tuple, Union

import pygame

from src.utils import easyTween
from src.utils.drawing import rendering

Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

particle_list = []
def update_particles(dt):
    for i in range(len(particle_list) - 1, -1, -1):
        particle = particle_list[i]
        particle.update(dt)
        if particle.done:
            particle_list.pop(i)
def draw_particles(renderer, camera):
    for particle in particle_list:
        particle.draw(renderer, camera)

class Particle:
    def __init__(self, x, y, size, speed, angle_deg, color: Color=None, image=None, lifetime=1, accel=0, fade=True, z=40):
        particle_list.append(self)
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.accel = accel
        self.angle = angle_deg
        self.color = color
        if color is not None and len(color) == 4:
            self.color = (color[0], color[1], color[2])
            self.alpha = color[3]
        else:
            self.alpha = 255
        self.lifetime = lifetime
        self.fade = fade
        self.z = z
        self.done = False

        self._image = image
        if image is not None:
            self._image = image
        elif color is not None:
            self._image = pygame.surface.Surface(size, pygame.SRCALPHA)
            self._image.fill(color)
        else:
            raise Exception("color and image cannot be None for Particle")

        easyTween.Timer(self, lifetime, "done", True)
        if self.fade:
            easyTween.Tween(self, "alpha", self.alpha, 0, self.lifetime)

    def update(self, dt):
        self.speed += self.accel * dt
        vx = math.cos(math.radians(self.angle)) * self.speed
        vy = math.sin(math.radians(self.angle)) * self.speed
        self.x += vx * dt
        self.y += vy * dt

    @property
    def image(self):
        img = self._image
        if self.color is not None:
            img.fill(self.color)
        return img

    def draw(self, renderer, camera):
        screen_pos = camera.to_screen((self.x, self.y))
        renderer.submit(rendering.DrawCmd(
            self.z,
            "smooth",
            self.image,
            screen_pos,
            alpha = self.alpha
        ))
