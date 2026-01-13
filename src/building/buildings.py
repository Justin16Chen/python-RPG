import pygame

from src.utils.drawing import rendering


class Base:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

        self.image = pygame.surface.Surface((32, 32))
        self.image.fill((255, 255, 255))

    def draw(self, camera, renderer):
        sx, sy = camera.to_screen((self.x, self.y))
        renderer.submit(rendering.DrawCmd(
            10, "pixel", self.image, (sx, sy)
        ))