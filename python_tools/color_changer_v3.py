"""Changes colors of images, preserving black, white and transparency. Changes only 'accent' color of each pixel"""

import os
import colorsys

from PIL import Image


def recolor_image_preserve_luminance(image_path: str,
                                     new_color: tuple[int, int, int]) -> None:
    """Changes image tint while preserving original brightness (black stays black)"""
    with Image.open(image_path).convert("RGBA") as im:
        pixels = im.load()
        width, height = im.size

        # Convert target color to HSL
        r_t, g_t, b_t = [x / 255.0 for x in new_color]
        h_target, s_target, _ = colorsys.rgb_to_hls(r_t, g_t, b_t)

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue

                # Normalize RGB
                r_n, g_n, b_n = [v / 255.0 for v in (r, g, b)]
                h, l, s = colorsys.rgb_to_hls(r_n, g_n, b_n)

                # If it's really black (low luminance), skip changing color
                if l < 0.05:
                    continue

                # Apply new hue and saturation, keep luminance
                r_new, g_new, b_new = colorsys.hls_to_rgb(h_target, l, s_target)
                pixels[x, y] = (
                    int(r_new * 255),
                    int(g_new * 255),
                    int(b_new * 255),
                    a
                )

        im.save(image_path)


def process_folder(folder_path: str, new_color: tuple[int, int, int]) -> None:
    """Recolors all .png images in the folder and its subfolders."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                image_path = os.path.join(root, file)
                print(f"Processing: {image_path}")
                recolor_image_preserve_luminance(image_path, new_color)


if __name__ == "__main__":
    target_folder = "C:/Users/DY/Pictures/Photoshop/WatchFace/Nixie_Tubes/Convertable"  # change this!
    blue   = (8, 141, 230)
    gray   = (222, 222, 222)
    yellow = (255, 237, 0)
    green  = (0, 255, 100)
    cian   = (8, 230, 189)

    new_rgb_color = gray
    process_folder(target_folder, new_rgb_color)
