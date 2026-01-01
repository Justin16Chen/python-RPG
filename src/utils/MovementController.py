import pygame

class MovementController:
    def __init__(self):
        self.vx = 0
        self.vy = 0

        self.max_speed = 300
        self.accel = 600
        self.friction_coeff = 0.7

        self.hitbox = pygame.rect.Rect(0, 0, 40, 40)

    def set_kinematics(self, max_speed, accel, friction_coeff):
        self.max_speed = max_speed
        self.accel = accel
        self.friction_coeff = friction_coeff

    def set_hitbox(self, w, h):
        self.hitbox.w = w
        self.hitbox.h = h

    def update_position(self, dt, move_dir):
        if move_dir.magnitude() != 0:
            move_dir = move_dir.normalize()
            x_dir = move_dir.x
            y_dir = move_dir.y
            self.vx += x_dir * self.accel
            self.vy += y_dir * self.accel

            self.vx = max(-self.max_speed, min(self.max_speed, self.vx))
            self.vy = max(-self.max_speed, min(self.max_speed, self.vy))

            if x_dir == 0:
                self.vx *= self.friction_coeff
            if y_dir == 0:
                self.vy *= self.friction_coeff
        else:
            self.vx *= self.friction_coeff
            self.vy *= self.friction_coeff

        self.x += self.vx * dt
        self.y += self.vy * dt

    @property
    def x(self):
        return self.hitbox.centerx
    @x.setter
    def x(self, value):
        self.hitbox.centerx = value
    @property
    def y(self):
        return self.hitbox.centery
    @y.setter
    def y(self, value):
        self.hitbox.centery = value