import pygame

from src.entity.player.Sword import Sword
from src.utils.MovementController import MovementController
from src.utils import InputController


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.move_controller = MovementController()
        self.move_controller.set_kinematics(100, 200, 0.7)
        self.move_controller.set_hitbox(20, 20)
        self.move_controller.x = 200
        self.move_controller.y = 200

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.image_rect = pygame.rect.Rect(0, 0, 20, 20)

        self.sword = Sword(game, self.move_controller.hitbox)
        self.sword.sword_offset = 12


    def update(self, dt, keys, mouse, mouse_pos):
        x_dir, y_dir = InputController.get_input_dir(keys)
        self.move_controller.update_position(dt, pygame.math.Vector2(x_dir, y_dir))

        if mouse.get_pressed()[0]:
            self.sword.swing()
        self.sword.update(dt, mouse_pos)

    def draw(self, screen):
        sx, sy = self.game.camera.to_screen((self.move_controller.x, self.move_controller.y))
        self.image_rect.center = (sx, sy)
        screen.blit(self.image, self.image_rect)

        self.sword.draw(screen)

