import os
from PIL import Image


def recolor_grayscale_to_transparent(image_path, new_color):
    with Image.open(image_path).convert("RGBA") as im:
        pixels = im.load()
        width, height = im.size

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]

                if a == 0:
                    continue  # skip fully transparent

                # Compute brightness (0 = black, 255 = white)
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                new_alpha = brightness  # black = 0, white = 255

                pixels[x, y] = (*new_color, new_alpha)

        im.save(image_path)


def process_folder(folder_path, new_color=(8, 230, 189)):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                image_path = os.path.join(root, file)
                print(f"Processing: {image_path}")
                recolor_grayscale_to_transparent(image_path, new_color)


if __name__ == "__main__":
    target_folder = "C:/Users/DY/Pictures/Photoshop/WatchFace/converter"
    new_rgb_color = (8, 230, 189)  # Target color
    process_folder(target_folder, new_rgb_color)
