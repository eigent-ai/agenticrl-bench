from PIL import Image, ImageDraw

# terrain.png: 256x128, 8 cols x 4 rows of 32x32 tiles, no margin/spacing
terrain = Image.new('RGBA', (256, 128), (40, 40, 40, 255))
draw = ImageDraw.Draw(terrain)
for col in range(8):
    for row in range(4):
        x, y = col * 32, row * 32
        color = ((col * 30 + row * 10) % 200 + 40,
                 (col * 20 + row * 40) % 200 + 40,
                 (col * 15 + row * 25) % 200 + 40, 255)
        draw.rectangle([x, y, x+31, y+31], fill=color, outline=(0, 0, 0, 255))
terrain.save('/game/src/tilesets/terrain.png')

# items.png: 180x90, 10 cols x 5 rows of 16x16 tiles, margin=1, spacing=2
# Width check: 2*1 + 10*16 + 9*2 = 2 + 160 + 18 = 180
# Height check: 2*1 + 5*16 + 4*2 = 2 + 80 + 8 = 90
items = Image.new('RGBA', (180, 90), (200, 200, 200, 255))
draw = ImageDraw.Draw(items)
for col in range(10):
    for row in range(5):
        x = 1 + col * (16 + 2)
        y = 1 + row * (16 + 2)
        color = ((col * 25) % 200 + 50,
                 (row * 50) % 200 + 50,
                 150, 255)
        draw.rectangle([x, y, x+15, y+15], fill=color)
items.save('/game/src/tilesets/items.png')

print("Tilesets generated successfully.")
