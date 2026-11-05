from PIL import Image

palette = [
    (255, 0,   0),    # 001 red
    (0,   200, 0),    # 002 green
    (0,   0,   255),  # 003 blue
    (255, 255, 0),    # 004 yellow
    (0,   255, 255),  # 005 cyan
    (255, 0,   255),  # 006 magenta
]

for i, c in enumerate(palette, 1):
    Image.new('RGB', (640, 480), color=c).save(
        f'/opt/media/frames/{i:03d}.jpg', 'JPEG', quality=95)
