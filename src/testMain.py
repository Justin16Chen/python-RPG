import pygame
from pygame import surface

from src.utils.drawing import drawing

pygame.init()

WIDTH, HEIGHT = 320*4, 180*4
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

world_grid = [
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
]

spritesheet = drawing.Spritesheet(drawing.load_image_asset("images/tilemaps/grassTilemap.png"), 8, 8)

tilemap = drawing.Tilemap(
    spritesheet,
    drawing.load_rule_asset("images/tilemaps/grassTilemapRules.json"),
)

surf = tilemap.get_grid_surface(world_grid, 64)
#surf = tilemap.spritesheet.get_frame(0, 3)
#surf = pygame.transform.scale(surf, (128, 128))
screen.blit(surf, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()