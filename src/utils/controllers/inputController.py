import pygame

def get_input_dir(keys):
    x_dir = 0
    y_dir = 0

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_dir += 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_dir -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y_dir += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y_dir -= 1

    return x_dir, y_dir
