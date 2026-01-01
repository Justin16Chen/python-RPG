import pygame

from src.utils.MovementController import MovementController
from src.utils import InputController


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.move_controller = MovementController()
        self.move_controller.set_kinematics(300, 600, 0.7)
        self.move_controller.set_hitbox(40, 40)
        self.move_controller.x = 400
        self.move_controller.y = 400

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 255))
        self.image_rect = pygame.rect.Rect(0, 0, 40, 40)


    def update(self, dt, keys):
        x_dir, y_dir = InputController.get_input_dir(keys)
        self.move_controller.update_position(dt, pygame.math.Vector2(x_dir, y_dir))

    def draw(self, screen):
        sx, sy = self.game.camera.to_screen((self.move_controller.x, self.move_controller.y))
        self.image_rect.center = (sx, sy)
        screen.blit(self.image, self.image_rect)

