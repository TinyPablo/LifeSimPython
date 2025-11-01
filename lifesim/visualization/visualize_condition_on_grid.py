from PIL import Image, ImageDraw
from lifesim.evolution.selection_conditions.enum import SelectionCondition
from utils import load_selection_condition_module

width, height = 200, 200
cell_size = 1

condition_enum = SelectionCondition.RIGHT_EDGE

mod = load_selection_condition_module(condition_enum.value)
condition = mod.condition

image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

meets = 0
for x in range(0, width, cell_size):
    for y in range(0, height, cell_size):
        if condition(x, y, width, height):
            meets += 1
            draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill="green")

print(f"Percentage of cells meeting condition: {meets / (width * height) * 100:.2f}%")
image.show()