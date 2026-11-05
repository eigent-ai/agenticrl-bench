from PIL import Image, ImageDraw

img = Image.new('RGB', (1600, 480), 'white')
draw = ImageDraw.Draw(img)
colors = ['red', 'green', 'blue', 'yellow', 'purple',
          'orange', 'cyan', 'magenta', 'lime', 'pink']
for idx in range(10):
    col = idx % 5
    row = idx // 5
    x = col * 320
    y = row * 240
    draw.rectangle([x, y, x + 319, y + 239], fill=colors[idx])
    draw.text((x + 130, y + 110), f'T{idx}', fill='black')
img.save('/workspace/spritesheet.png')
