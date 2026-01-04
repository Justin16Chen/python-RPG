import json
from pathlib import Path

import pygame

from src.utils.drawing import rendering


class World:
    def __init__(self, game):
        self.level_data = None

    def load_room(self, room_x, room_y):
        root = Path(__file__).resolve().parents[2]
        path = root / "assets" / "rooms" / f"r{room_x}{room_y}.json"
        print(path)
        with open(path, "r") as file:
            self.level_data = json.load(file)

        self._reload_tile_surfaces()

    def _reload_tile_surfaces(self):
        self.tile_surfaces = {
            0: pygame.Surface((self.tile_size, self.tile_size)),
            1: pygame.Surface((self.tile_size, self.tile_size)),
        }
        self.tile_surfaces[0].fill((30, 30, 30))
        self.tile_surfaces[1].fill((0, 0, 0))

    @property
    def tile_size(self):
        return self.level_data["tile size"]
    @property
    def tile_data(self):
        return self.level_data["data"]
    @property
    def right_bound(self):
        return len(self.tile_data[0]) * self.tile_size
    @property
    def bottom_bound(self):
        return len(self.tile_data) * self.tile_size
    @property
    def player_spawn_position(self):
        return self.level_data["player spawn"][0] * self.tile_size, self.level_data["player spawn"][1] * self.tile_size

    def world_pos_to_grid(self, world_pos):
        return world_pos[0] // self.tile_size, world_pos[1] // self.tile_size

    def clamp_grid_pos(self, grid_pos):
        return max(0, min(grid_pos[0], len(self.tile_data[0]))), max(0, min(grid_pos[1], len(self.tile_data)))

    def draw(self, renderer, camera):
        ts = self.tile_size
        min_grid_x, min_grid_y = self.clamp_grid_pos(self.world_pos_to_grid((camera.x, camera.y)))
        max_grid_x, max_grid_y = self.clamp_grid_pos(self.world_pos_to_grid((camera.x + camera.screen_w + ts, camera.y + camera.screen_h + ts)))

        for y in range(min_grid_y, max_grid_y):
            for x in range(min_grid_x, max_grid_x):
                tile = self.tile_data[y][x]

                draw_x = x * ts - camera.x
                draw_y = y * ts - camera.y

                renderer.submit(rendering.DrawCmd(0, "pixel", self.tile_surfaces[tile], (draw_x, draw_y), anchor="topleft"))
