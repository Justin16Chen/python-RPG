class Animation:
    def __init__(self, frames, fps=12, loop=False):
        self.frames = frames
        self.loop = loop
        self.frame_time = 1.0 / fps
        self.time_acc = 0.0
        self.index = 0
        self.done = False

    def update(self, dt):
        if self.done:
            return

        self.time_acc += dt
        while self.time_acc >= self.frame_time:
            self.time_acc -= self.frame_time
            self.index += 1

            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.done = True

    @property
    def image(self):
        return self.frames[self.index]
