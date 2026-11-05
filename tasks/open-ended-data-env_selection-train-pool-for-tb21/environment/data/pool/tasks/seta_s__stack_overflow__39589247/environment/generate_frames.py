from PIL import Image, ImageDraw

for i in range(10):
    img = Image.new("RGB", (320, 240), (0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 159, 139], fill=(255, 0, 0))
    draw.ellipse([200, 150, 250, 190], fill=(0, 255, 0))
    img.save(f"frames/frame_{i:03d}.png")

print("Generated 10 frames")
