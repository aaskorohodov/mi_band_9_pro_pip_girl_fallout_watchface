import os
from PIL import Image
import colorsys


def is_grayscale(color: tuple[int, int, int]) -> bool:
    """Returns True if the RGB color is grayscale (R==G==B)."""
    r, g, b = color
    return r == g == b


def recolor_image_preserve_luminance(image_path: str,
                                     new_color: tuple[int, int, int]) -> None:
    """Changes image tint while preserving original brightness (black stays black)"""
    with Image.open(image_path).convert("RGBA") as im:
        pixels = im.load()
        width, height = im.size

        if is_grayscale(new_color):
            # Use simple grayscale recoloring
            gray_value = new_color[0] / 255.0  # since R==G==B
            for y in range(height):
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    if a == 0:
                        continue

                    r_n, g_n, b_n = [v / 255.0 for v in (r, g, b)]
                    _, l, _ = colorsys.rgb_to_hls(r_n, g_n, b_n)

                    if l < 0.05:
                        continue

                    gray_pixel = int(l * gray_value * 255)
                    pixels[x, y] = (gray_pixel, gray_pixel, gray_pixel, a)
        else:
            # Convert target color to HLS
            r_t, g_t, b_t = [x / 255.0 for x in new_color]
            h_target, s_target, _ = colorsys.rgb_to_hls(r_t, g_t, b_t)

            for y in range(height):
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    if a == 0:
                        continue

                    r_n, g_n, b_n = [v / 255.0 for v in (r, g, b)]
                    h, l, s = colorsys.rgb_to_hls(r_n, g_n, b_n)

                    if l < 0.05:
                        continue

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
    gray   = (255, 255, 255)
    yellow = (255, 237, 0)
    green  = (0, 255, 100)
    cian   = (8, 230, 189)

    new_rgb_color = gray
    process_folder(target_folder, new_rgb_color)
