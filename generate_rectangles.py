import os
import json
import random
from PIL import Image

# Define the output directories for the PNG and JSON files
png_output_dir = "output/png"
json_output_dir = "output/json"

if not os.path.exists(png_output_dir):
    os.makedirs(png_output_dir)

if not os.path.exists(json_output_dir):
    os.makedirs(json_output_dir)

# Define the size of the images
image_size = 30

# Generate 5000 PNG and JSON files
for i in range(10000):
    # Generate random position and size for the black rectangle
    rectangle_width = random.randint(3, image_size-2) # at least 1px padding at each side
    rectangle_height = random.randint(3, image_size-2)
    rectangle_x1 = random.randint(1, image_size-rectangle_width-1)
    rectangle_y1 = random.randint(1, image_size-rectangle_height-1)
    rectangle_x2 = rectangle_x1 + rectangle_width
    rectangle_y2 = rectangle_y1 + rectangle_height

    # Create a white image with a black rectangle
    img = Image.new("RGB", (image_size, image_size), color="white")
    for x in range(rectangle_x1, rectangle_x2):
        for y in range(rectangle_y1, rectangle_y2):
            img.putpixel((x, y), (0, 0, 0))

    # Generate a filename for the PNG and JSON files
    filename = os.path.join(png_output_dir, f"{os.urandom(16).hex()}.png")

    # Save the PNG file
    img.save(filename)

    # Generate the JSON data
    json_data = {
        "verts": [[rectangle_x1, rectangle_y1], [rectangle_x2-1, rectangle_y1],
                  [rectangle_x2-1, rectangle_y2-1], [rectangle_x1, rectangle_y2-1]]
    }

    # Save the JSON file
    json_filename = os.path.splitext(filename)[0] + ".json"
    json_filename = json_filename.replace("png", "json")
    with open(json_filename, "w") as f:
        json.dump(json_data, f)
