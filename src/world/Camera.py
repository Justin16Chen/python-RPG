
class Camera:
    def __init__(self, screen_width, screen_height, x, y):
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.x = x
        self.y = y

        self.parent = None
        self.right_bound = None
        self.bottom_bound = None

    def set_bounds(self, right_bound, bottom_bound):
        self.right_bound = right_bound - self.screen_w
        self.bottom_bound = bottom_bound - self.screen_h

    def follow(self, obj):
        self.parent = obj

    def update(self):
        if self.parent is not None:
            self.x = self.parent.x - self.screen_w // 2
            self.y = self.parent.y - self.screen_h // 2

        if self.right_bound is not None and self.bottom_bound is not None:
            self.x = max(0, min(self.right_bound, self.x))
            self.y = max(0, min(self.bottom_bound, self.y))

    def to_screen(self, world_pos):
        return int(world_pos[0] - self.x), int(world_pos[1] - self.y)
