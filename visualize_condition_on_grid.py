from PIL import Image, ImageDraw

# Define the width and height of the image
width, height = 200,200

# Create a new image with a white background
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Define the condition function
def condition(x, y, w, h):
    square_w = w // 8
    square_h = h // 8

    return (
        # Top wall center
        ((w // 2 - square_w // 2 <= x <= w // 2 + square_w // 2) and (y <= square_h)) or
        # Bottom wall center
        ((w // 2 - square_w // 2 <= x <= w // 2 + square_w // 2) and (y >= h - square_h)) or
        # Left wall center
        ((x <= square_w) and (h // 2 - square_h // 2 <= y <= h // 2 + square_h // 2)) or
        # Right wall center
        ((x >= w - square_w) and (h // 2 - square_h // 2 <= y <= h // 2 + square_h // 2))
    )

# Define the size of each grid cell
cell_size = 1  # You can adjust this value as needed

meets = 0
# Loop over the grid cells
for x in range(0, width, cell_size):
    for y in range(0, height, cell_size):
        if condition(x, y, width, height):
            meets += 1
            draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill="red")

print(meets / (width * height) * 100)

# Save the image
image.save("grid_image.png")

# Optionally, show the image
image.show()
