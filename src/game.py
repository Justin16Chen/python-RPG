import pygame

from src.entity.player.player import Player
from src.world.camera import Camera
from src.world.world import World


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height


        self.world = World(self)
        self.world.load_room(0, 0)

        self.player = Player(self)
        spawn = self.world.player_spawn_position
        self.player.move_controller.x = spawn[0]
        self.player.move_controller.y = spawn[1]

        self.camera = Camera(screen_width, screen_height, 0, 0)
        self.camera.set_bounds(self.world.right_bound, self.world.bottom_bound)
        self.camera.follow(self.player.move_controller)


    def update(self, dt, mouse_pos):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse
        self.player.update(dt, keys, mouse, mouse_pos)
        self.camera.update()

    def draw(self, renderer):
        self.world.draw(renderer, self.camera)
        self.player.draw(renderer)
