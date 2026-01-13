import pygame


class Mouse:
    def __init__(self, mouse):
        self.mouse = mouse
        self.draw_scale = 1
        self.lb_frames_down = 0

    def update(self, draw_scale):
        self.draw_scale = draw_scale
        if pygame.mouse.get_pressed()[0]:
            self.lb_frames_down += 1
        else:
            self.lb_frames_down = 0

    @property
    def x(self):
        return pygame.mouse.get_pos()[0] / self.draw_scale
    @property
    def y(self):
        return pygame.mouse.get_pos()[1] / self.draw_scale

    @property
    def lb_first(self):
        return self.lb_frames_down == 1

    @property
    def lb_down(self):
        return self.lb_frames_down > 0
