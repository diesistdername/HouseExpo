import os
import json
import random
from PIL import Image, ImageDraw

def generate_rect(image_size):
    rectangle_width = random.randint(3, image_size-2)
    rectangle_height = random.randint(3, image_size-2)
    rectangle_x1 = random.randint(1, image_size-rectangle_width-1)
    rectangle_y1 = random.randint(1, image_size-rectangle_height-1)
    rectangle_x2 = rectangle_x1 + rectangle_width
    rectangle_y2 = rectangle_y1 + rectangle_height
    rectangle_verts = [(rectangle_x1, rectangle_y1),
                       (rectangle_x2-1, rectangle_y1),
                       (rectangle_x2-1, rectangle_y2-1),
                       (rectangle_x1, rectangle_y2-1)]
    return rectangle_verts

def has_overlap(verts1, verts2):
    for v1 in verts1:
        for v2 in verts2:
            if v1[0] <= v2[0] <= v1[0] + 1 and v1[1] <= v2[1] <= v1[1] + 1:
                return True
    return False

# Define the output directories for the PNG and JSON files
png_output_dir = "output/png"
json_output_dir = "output/json"

if not os.path.exists(png_output_dir):
    os.makedirs(png_output_dir)

if not os.path.exists(json_output_dir):
    os.makedirs(json_output_dir)

# Define the size of the images
image_size = 30

# Generate 50 PNG and JSON files
generated_images = 0
while generated_images < 50:
    # Generate random position and size for the rectangles
    num_rectangles = random.randint(1, 3)
    rectangles = []
    img = Image.new("RGB", (image_size, image_size), color="white")
    draw = ImageDraw.Draw(img)

    for i in range(num_rectangles):
        if i != 0:
            has_overlap_flag = False
            while not has_overlap_flag:
                rectangle_verts = generate_rect(image_size)

                for existing_rect in rectangles:
                    if has_overlap(rectangle_verts, existing_rect):
                        has_overlap_flag = True
                        break
                else:
                    has_overlap_flag = False

        else:
            rectangle_verts = generate_rect(image_size)

        draw.polygon(rectangle_verts, outline=(0, 0, 0), fill=(0, 0, 0))
        rectangles.append(rectangle_verts)

    print(rectangles)    

    filename = os.urandom(16).hex()
    pngDir = os.path.join(png_output_dir, f"{filename}.png")
    jsonDir = os.path.join(json_output_dir, f"{filename}.json")


    img.save(pngDir)

    json_data = {"verts": rectangle_verts}
    with open(jsonDir, "w") as f:
        json.dump(json_data, f)

    generated_images += 1