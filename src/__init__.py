import pygame
import sys
from src.Game import Game
from src.utils.easyTween import Tween, Timer

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")

clock = pygame.time.Clock()
FPS = 60

game = Game(WIDTH, HEIGHT)

running = True
while running:
    dt = clock.tick(FPS) / 1000.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Tween.update_tweens(dt)
    Timer.update_timers(dt)
    game.update(dt)

    screen.fill((30, 30, 30))
    game.draw(screen)
    pygame.display.flip()


pygame.quit()
sys.exit()
