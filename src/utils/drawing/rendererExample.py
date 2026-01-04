import pygame as pg
from rendering import Renderer, DrawCmd

pg.init()

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
V_W, V_H = 320, 180
SCALE = 4
WIN_W, WIN_H = V_W * SCALE, V_H * SCALE

screen = pg.display.set_mode((WIN_W, WIN_H))
clock = pg.time.Clock()

renderer = Renderer(scale=SCALE)

# -------------------------------------------------------------------
# ASSETS (dummy colored surfaces for example)
# -------------------------------------------------------------------
def make_box(size, color):
    surf = pg.Surface(size, pg.SRCALPHA)
    surf.fill(color)
    return surf

player_img = make_box((16, 16), (80, 200, 255))
ship_img   = make_box((24, 12), (220, 120, 60))
icon_img   = make_box((6, 6),   (255, 255, 0))
tile_img   = make_box((16, 16), (40, 40, 40))

# -------------------------------------------------------------------
# WORLD STATE
# -------------------------------------------------------------------
player_pos = pg.Vector2(80, 80)
ship_pos   = pg.Vector2(140, 90)
ship_angle = 0.0

cam = pg.Vector2(0, 0)

# -------------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------------
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    # ----------------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------------
    keys = pg.key.get_pressed()
    if keys[pg.K_a]: player_pos.x -= 80 * dt
    if keys[pg.K_d]: player_pos.x += 80 * dt
    if keys[pg.K_w]: player_pos.y -= 80 * dt
    if keys[pg.K_s]: player_pos.y += 80 * dt

    ship_angle += 90 * dt

    # camera follows player (float camera!)
    cam = player_pos - pg.Vector2(V_W / 2, V_H / 2)

    # ----------------------------------------------------------------
    # DRAW
    # ----------------------------------------------------------------
    screen.fill((10, 10, 12))
    renderer.begin()

    # --- background tiles (pixel-perfect) ---
    for y in range(0, 12):
        for x in range(0, 20):
            renderer.submit(DrawCmd(
                z=0,
                kind="pixel",
                image=tile_img,
                draw_pos=pg.Vector2(x * 16, y * 16),
                anchor="topleft"
            ))


    # --- UI/icon drawn on top of ship but NOT rotated ---
    renderer.submit(DrawCmd(
        z=30,
        kind="smooth",
        image=icon_img,
        draw_pos=ship_pos + pg.Vector2(0, -14),
        anchor="center"
    ))
    # --- smooth rotated ship (above player) ---
    renderer.submit(DrawCmd(
        z=20,
        kind="smooth",
        image=ship_img,
        draw_pos=ship_pos,
        anchor="center",
        angle_deg=ship_angle
    ))
    # --- player (pixel-perfect, above tiles) ---
    renderer.submit(DrawCmd(
        z=10,
        kind="pixel",
        image=player_img,
        draw_pos=player_pos,
        anchor="center"
    ))


    renderer.flush(screen, cam)
    pg.display.flip()

pg.quit()
