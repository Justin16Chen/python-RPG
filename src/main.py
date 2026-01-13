import pygame
import sys
from src.game import Game
from src.utils import particles, inputs
from src.utils.drawing import rendering, resizing
from src.utils.easyTween import Tween, Timer


pygame.init()

WIDTH, HEIGHT = 320, 180
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("python RPG")

clock = pygame.time.Clock()
FPS = 60

mouse = inputs.Mouse(pygame.mouse)
game = Game(WIDTH, HEIGHT)
renderer = rendering.Renderer()


running = True
while running:
    dt = clock.tick(FPS) / 1000.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            width = max(WIDTH, width)
            height = max(HEIGHT, height)
            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

    draw_scale, x_draw_offset, y_draw_offset = resizing.calculate_draw_info(WIDTH, HEIGHT)
    renderer.draw_scale = draw_scale

    mouse.update(draw_scale)

    Tween.update_tweens(dt)
    Timer.update_timers(dt)
    particles.update_particles(dt)
    game.update(dt, mouse)

    screen.fill((129, 153, 54))
    renderer.begin()
    particles.draw_particles(renderer, game.camera)
    game.draw(renderer)

    renderer.flush(screen, x_draw_offset, y_draw_offset)
    resizing.draw_black_bars(screen, x_draw_offset, y_draw_offset)
    pygame.display.flip()

pygame.quit()
sys.exit()
