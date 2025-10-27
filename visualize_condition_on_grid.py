from PIL import Image, ImageDraw


width, height = 200,200

image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

def condition(x, y, w, h):
    return (w // 3 <= x < 2 * w // 3) and (h // 3 <= y < 2 * h // 3)



cell_size = 1 

meets = 0

for x in range(0, width, cell_size):
    for y in range(0, height, cell_size):
        if condition(x, y, width, height):
            meets += 1
            draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill="green")

print(meets / (width * height) * 100)

image.show()
