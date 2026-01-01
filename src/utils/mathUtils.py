import pygame

def get_collision_dir(rect1: pygame.Rect, rect2: pygame.Rect) -> pygame.math.Vector2:
    """
    Returns a cardinal direction unit vector indicating the collision side of rect2 w.r.t rect1.
    (1,0)=rect2 is to the right, (-1,0)=left, (0,1)=below, (0,-1)=above.

    Assumes rects overlap (or at least are close); best used after collision is detected.
    """

    # Centers
    c1x, c1y = rect1.centerx, rect1.centery
    c2x, c2y = rect2.centerx, rect2.centery

    dx = c2x - c1x
    dy = c2y - c1y

    # Amount of overlap along each axis (positive means overlapping if they collide)
    overlap_x = (rect1.width / 2 + rect2.width / 2) - abs(dx)
    overlap_y = (rect1.height / 2 + rect2.height / 2) - abs(dy)

    # If they don't overlap, fall back to "which direction is rect2" based on centers
    if overlap_x <= 0 or overlap_y <= 0:
        if abs(dx) > abs(dy):
            return pygame.math.Vector2(1, 0) if dx > 0 else pygame.math.Vector2(-1, 0)
        else:
            return pygame.math.Vector2(0, 1) if dy > 0 else pygame.math.Vector2(0, -1)

    # Collision normal is along the axis of least penetration
    if overlap_x < overlap_y:
        return pygame.math.Vector2(1, 0) if dx > 0 else pygame.math.Vector2(-1, 0)
    else:
        return pygame.math.Vector2(0, 1) if dy > 0 else pygame.math.Vector2(0, -1)


def lerp(a, b, t):
    return a + (b - a) * t
