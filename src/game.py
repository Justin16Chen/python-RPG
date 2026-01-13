import pygame

from src.building import buildings
from src.entity.player.player import Player
from src.world.camera import Camera
from src.world.world import World


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.world = World()
        self.world.load_room(0, 0)

        self.player = Player(self, self.world.get_entity_position("player"))
        self.base = buildings.Base(self.world.get_entity_position("base"))

        self.camera = Camera(screen_width, screen_height, 0, 0)
        self.camera.set_bounds(self.world.right_bound, self.world.bottom_bound)
        self.camera.follow(self.player.move_controller)


    def update(self, dt, mouse):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, mouse)
        self.camera.update()

    def draw(self, renderer):
        self.world.draw(renderer, self.camera)
        self.player.draw(renderer)
        self.base.draw(self.camera, renderer)
