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

upperBoundX = 30
upperBoundY = upperBoundX
# Generate 1000 PNG and JSON files
for i in range(5000):
    # Generate a random position for the black pixel
    black_pixel_posX = random.randint(0, upperBoundX-1)
    black_pixel_posY = random.randint(0, upperBoundY-1)

    # Create a white image with one black pixel
    img = Image.new("RGB", (upperBoundX, upperBoundY), color="white")
    img.putpixel((black_pixel_posX, black_pixel_posY), (0, 0, 0))

    # Generate a filename for the PNG and JSON files
    filename = os.path.join(png_output_dir, f"{os.urandom(16).hex()}.png")

    # Save the PNG file
    img.save(filename)

    # Generate the JSON data
    json_data = {
        "verts": [[black_pixel_posX, black_pixel_posY]]
        #,"id": os.path.splitext(os.path.basename(filename))[0]
    }

    # Save the JSON file
    json_filename = os.path.splitext(filename)[0] + ".json"
    json_filename = json_filename.replace("png", "json")
    with open(json_filename, "w") as f:
        json.dump(json_data, f)
