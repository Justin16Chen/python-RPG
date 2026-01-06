import pygame as pg
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class DrawCmd:
    z: int
    kind: str   # "pixel" or "smooth"
    image: pg.Surface
    draw_pos: tuple[float, float]
    anchor: str = "center"
    angle_deg: float = 0.0
    scale: float = 1.0
    alpha: int = 255
    force_refresh: bool = False

class Renderer:
    def __init__(self: int):
        self.draw_scale = 1 # scale from virtual game pixel screen to actual display screen
        self.queue = []
        self._pixel_scale_cache: Dict[Tuple[int,str,float,str,int], pg.Surface] = {}
        self._pad_cache = {}

    def begin(self):
        self.queue.clear()

    def submit(self, cmd: DrawCmd):
        self.queue.append(cmd)

    def _get_scaled_pixel_sprite(self, c: DrawCmd) -> pg.Surface:
        key = (id(c.image), c.anchor, c.scale, c.kind, self.draw_scale)
        cached = self._pixel_scale_cache.get(key)
        if cached is None or c.force_refresh:
            w, h = c.image.get_size()
            cached = pg.transform.scale(c.image, (w * self.draw_scale, h * self.draw_scale)).convert_alpha()
            self._pixel_scale_cache[key] = cached
        return cached

    def _get_padded(self, c: DrawCmd, pad: int = 2) -> pg.Surface:
        key = (id(c.image), pad)
        cached = self._pad_cache.get(key)
        if cached is None or c.force_refresh:
            w, h = c.image.get_size()
            padded = pg.Surface((w + pad * 2, h + pad * 2), pg.SRCALPHA)
            padded.blit(c.image, (pad, pad))
            cached = padded.convert_alpha()
            self._pad_cache[key] = cached
        return cached

    def _rect_for_anchor(self, img: pg.Surface, anchor: str, x: float, y: float) -> pg.Rect:
        if anchor == "center":
            return img.get_rect(center=(x, y))
        return img.get_rect(topleft=(x, y))

    def flush(self, screen: pg.Surface, x_draw_offset, y_draw_offset):
        self.queue.sort(key=lambda command: command.z)

        for c in self.queue:
            if c.kind == "pixel":
                sx = int(c.draw_pos[0]) * self.draw_scale
                sy = int(c.draw_pos[1]) * self.draw_scale

                img = self._get_scaled_pixel_sprite(c)
                img = pg.transform.rotate(img, -c.angle_deg)
                img.set_alpha(c.alpha)
                r = self._rect_for_anchor(img, c.anchor, sx, sy)
                r.x += x_draw_offset
                r.y += y_draw_offset
                screen.blit(img, r)

            else:  # smooth
                sx = c.draw_pos[0] * self.draw_scale
                sy = c.draw_pos[1] * self.draw_scale

                base = self._get_padded(c, pad=2)
                base.set_alpha(c.alpha)

                # 1) scale up with NEAREST (keeps sprite crisp before rotation)
                w, h = base.get_size()
                scaled_base = pg.transform.scale(base, (int(w * self.draw_scale * c.scale), int(h * self.draw_scale * c.scale)))

                # 2) rotate WITHOUT additional scaling (keeps it from getting blurrier)
                img = pg.transform.rotate(scaled_base, c.angle_deg)

                r = self._rect_for_anchor(img, c.anchor, sx, sy)
                r.x += x_draw_offset
                r.y += y_draw_offset
                screen.blit(img, r)
