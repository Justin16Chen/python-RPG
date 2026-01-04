import pygame

def calculate_draw_info(pixel_width, pixel_height):
    monitor_info = pygame.display.Info()
    monitor_width = monitor_info.current_w
    monitor_height = monitor_info.current_h

    draw_scale = min(monitor_width / pixel_width, monitor_height / pixel_height)

    game_width = int(pixel_width * draw_scale)
    game_height = int(pixel_height * draw_scale)
    x_draw_offset = int((monitor_width - game_width) / 2)
    y_draw_offset = int((monitor_height - game_height) / 2)

    return draw_scale, x_draw_offset, y_draw_offset

def draw_black_bars(screen, bar_width, bar_height):
    monitor_info = pygame.display.Info()
    monitor_width = monitor_info.current_w
    monitor_height = monitor_info.current_h

    rect1 = None
    rect2 = None
    if bar_width > 0:
        rect1 = pygame.Rect(0, 0, bar_width, monitor_height)
        rect2 = pygame.Rect(monitor_width - bar_width, 0, bar_width, monitor_height)
    elif bar_height > 0:
        rect1 = pygame.Rect(0, 0, monitor_width, bar_height)
        rect2 = pygame.Rect(0, monitor_height - bar_height, monitor_width, bar_height)

    if rect1 is not None:
        black_bar_image = pygame.surface.Surface(rect1.size)
        black_bar_image.fill((0, 0, 0))
        screen.blit(black_bar_image, rect1)
        screen.blit(black_bar_image, rect2)