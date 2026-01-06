from pathlib import Path

import pygame

from src.entity.player.sword import Sword
from src.utils.controllers import inputController
from src.utils.controllers.movementController import MovementController
from src.utils.drawing import rendering, drawing


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.move_controller = MovementController()
        self.move_controller.set_kinematics(100, 200, 0.7)
        self.move_controller.set_hitbox(20, 20)
        self.move_controller.x = 200
        self.move_controller.y = 200

        root = Path(__file__).resolve().parents[3]
        path = root / "assets" / "images" / "entities" / "player animation.png"
        anim_info = [
            drawing.AnimInfo("idle", 1, 12),
            drawing.AnimInfo("jump", 1, 12),
            drawing.AnimInfo("run", 3, 12, loop=True, ping_pong=True)
        ]
        spritesheet = drawing.SpriteSheet(pygame.image.load(path).convert_alpha(), 16, 16)
        self.anim_manager = drawing.AnimationManager(spritesheet, anim_info)

        self.sword = Sword(game, self.move_controller.hitbox)
        self.sword.sword_offset = 12

    def update(self, dt, keys, mouse, mouse_pos):

        # update movement
        x_dir, y_dir = inputController.get_input_dir(keys)
        self.move_controller.update_position(dt, pygame.math.Vector2(x_dir, y_dir))

        # update sword
        if mouse.get_pressed()[0]:
            self.sword.swing()
        self.sword.update(dt, mouse_pos)

        # update animations
        if x_dir == 0 and y_dir == 0:
            self.anim_manager.set_anim("idle")
        else:
            self.anim_manager.set_anim("run")
        if x_dir != 0:
            self.anim_manager.cur_anim.flip_x = x_dir < 0
        self.anim_manager.update(dt)

    def draw(self, renderer):
        screen_pos = self.game.camera.to_screen((self.move_controller.x, self.move_controller.y))
        renderer.submit(rendering.DrawCmd(10, "pixel", self.anim_manager.cur_anim.image, screen_pos))
        self.sword.draw(renderer)
