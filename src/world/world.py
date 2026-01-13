import json
import random
from pathlib import Path

import pygame

from src.utils.drawing import rendering, drawing


class World:
    def __init__(self):
        self.level_data = None
        image = drawing.load_image_asset("images/tilemaps/grassTilemap.png")
        self.tile_spritesheet = drawing.Spritesheet(image, 8, 8)
        self.tile_data_dict = {
            1: [(1, 0), (2, 0)],
            2: [(0, 1), (0, 2)],
            3: [(4, 1), (4, 2)],
            4: [(1, 5), (1, 5)]
        }
        self.tile_draw_data = []

    def load_room(self, room_x, room_y):
        root = Path(__file__).resolve().parents[2]
        path = root / "assets" / "rooms" / f"r{room_x}{room_y}.json"
        with open(path, "r") as file:
            self.level_data = json.load(file)
            self.tile_draw_data = []
            for y in range(len(self.tile_data)):
                self.tile_draw_data.append([])
                for x in range(len(self.tile_data[0])):
                    tile = self.tile_data[y][x]
                    if tile == 0:
                        self.tile_draw_data[y].append(None)
                    else:
                        variants = self.tile_data_dict[tile]
                        print(f"possible variants: {variants}")
                        variant = random.choice(variants)
                        print(f"chosen variant: {variant}")
                        self.tile_draw_data[y].append(variant)

    @property
    def tile_size(self):
        return self.level_data["tile size"]
    @property
    def tile_data(self):
        return self.level_data["tile data"]
    @property
    def right_bound(self):
        return len(self.tile_data[0]) * self.tile_size
    @property
    def bottom_bound(self):
        return len(self.tile_data) * self.tile_size

    def get_entity_position(self, entity_name):
        return self.level_data["entity data"][entity_name][0] * self.tile_size, self.level_data["entity data"][entity_name][1] * self.tile_size

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

                draw_x = x * ts - camera.x
                draw_y = y * ts - camera.y
                tilemap_pos = self.tile_draw_data[y][x]
                if tilemap_pos is not None:
                    renderer.submit(rendering.DrawCmd(0, "pixel", self.tile_spritesheet.get_frame(tilemap_pos[0], tilemap_pos[1]), (draw_x, draw_y), anchor="topleft"))
