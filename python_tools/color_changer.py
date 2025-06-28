"""Changes color of images, designed for change colors to GRAY specifically

IMPORTANT: changes all pixels to desired color."""

import os

from PIL import Image


def recolor_image(image_path: str,
                  new_color: tuple[int, int, int]) -> None:
    """Changes color of provided image

    Args:
        image_path: Path to image to change color of
        new_color: New color im RGB-format"""

    with Image.open(image_path).convert("RGBA") as im:
        pixels = im.load()
        width, height = im.size

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a != 0:  # Only change visible pixels
                    pixels[x, y] = (*new_color, a)

        im.save(image_path)


def process_folder(folder_path: str,
                   new_color: tuple[int, int, int]) -> None:
    """Searches all png-files in folder AND ALL OF ITS SUBFOLDERS and changes color

    Args:
        folder_path: Path to search all png-files in
        new_color: New color for images in RGB-format"""

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                image_path = os.path.join(root, file)
                print(f"Processing: {image_path}")
                recolor_image(image_path, new_color)


if __name__ == "__main__":
    target_folder = r"C:\Users\DY\PycharmProjects\mi_band_9_pro_pip_girl_fallout_watchface\media_src\converter"  # ← change this!
    blue   = (8, 141, 230)
    gray   = (222, 222, 222)
    yellow = (255, 237, 0)
    orange = (255, 80, 0)
    new_rgb_color = orange
    process_folder(target_folder, new_rgb_color)
