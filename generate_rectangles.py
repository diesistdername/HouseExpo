import os
import json
import random
from PIL import Image, ImageDraw

def is_rectangle_intersecting(rectangle1, rectangle2):
    """
    Check if two rectangles intersect.
    """
    x1, y1 = rectangle1[0]
    x2, y2 = rectangle1[2]
    x3, y3 = rectangle2[0]
    x4, y4 = rectangle2[2]

    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

def get_intersection(rectangle1, rectangle2):
    """
    Get the intersection points of two rectangles.
    """
    x1, y1 = rectangle1[0]
    x2, y2 = rectangle1[2]
    x3, y3 = rectangle2[0]
    x4, y4 = rectangle2[2]

    x_left = max(x1, x3)
    x_right = min(x2, x4)
    y_bottom = max(y1, y3)
    y_top = min(y2, y4)

    return [(x_left, y_bottom), (x_right, y_top)]


def is_vertex_contained(vertex, rectangle):
    """
    Check if a vertex is contained in a rectangle.
    """
    x, y = vertex
    x1, y1 = rectangle[0]
    x2, y2 = rectangle[2]
    return x1 <= x <= x2 and y1 <= y <= y2

def get_outer_points_and_intersections(rectangles):
    points = []
    if(len(rectangles) == 1):
        points.append(rectangles[0])
    else:
        for i, rectangle in enumerate(rectangles):
            for j, other_rectangle in enumerate(rectangles):
                if j > i:
                    if is_rectangle_intersecting(rectangle, other_rectangle):
                        left, right = get_intersection(rectangle, other_rectangle)
                        points.append(left)
                        points.append(right)
                if j != i:
                    for vertex in rectangle:
                        if not is_vertex_contained(vertex, other_rectangle):
                            points.append(vertex)    
    return points



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

    outerPoints = get_outer_points_and_intersections(rectangles)
    if(generated_images<5):
        print("rectangles:",rectangles)
        print("outerPoints:",outerPoints)
        print("-------------------")

    filename = os.urandom(16).hex()
    pngDir = os.path.join(png_output_dir, f"{filename}.png")
    jsonDir = os.path.join(json_output_dir, f"{filename}.json")


    img.save(pngDir)

    json_data = {"verts": outerPoints}
    with open(jsonDir, "w") as f:
        json.dump(json_data, f)

    generated_images += 1