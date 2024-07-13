from screeninfo import get_monitors

WIN_SIZE = 0, 0
for m in get_monitors():
    if not m.is_primary:
        continue
    if m.width >= 1920 and m.height >= 1080:
        WIN_SIZE = 1920, 1080
    else:
        WIN_SIZE = 1280, 720

SCN_SIZE = 240, 135
FACTOR = WIN_SIZE[0] / SCN_SIZE[0]
GRAVITY = 9.8 * 16
ROOM_TOPLEFT = (32, 28)
ROOM_BOTTOMRIGHT = (208, 108)
COLOR_SETS = [
    [
        # Grey
        (26, 12, 49),
        (53, 54, 88),
        (104, 107, 114),
        (136, 151, 185),
        (195, 205, 220),
        (255, 255, 255),
    ],
    [
        # Red
        (30, 9, 13),
        (114, 13, 13),
        (140, 49, 0),
        (238, 0, 14),
    ],
    [
        # Blue
        (0, 51, 58),
        (14, 50, 174),
        (0, 147, 226),
        (0, 237, 235),
    ],
    [
        # Green
        (0, 51, 58),
        (0, 95, 65),
        (8, 178, 59),
        (71, 246, 65),
    ],
    [
        # Yellow
        (114, 13, 13),
        (239, 110, 16),
        (236, 171, 17),
        (236, 233, 16)
    ],
]
