import pygame
import sys
from src.Game import Game
from src.utils.EasyTween import Tween, Timer


pygame.init()

WIDTH, HEIGHT = 640, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("python RPG")

game_surface = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

game = Game(WIDTH, HEIGHT)

running = True
while running:
    dt = clock.tick(FPS) / 1000.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    monitor_info = pygame.display.Info()
    monitor_width = monitor_info.current_w
    monitor_height = monitor_info.current_h
    scale = min(monitor_width / WIDTH, monitor_height / HEIGHT)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x /= scale
    mouse_y /= scale

    Tween.update_tweens(dt)
    Timer.update_timers(dt)
    game.update(dt, (mouse_x, mouse_y))

    game_surface.fill((30, 30, 30))
    game.draw(game_surface)

    scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()


pygame.quit()
sys.exit()
