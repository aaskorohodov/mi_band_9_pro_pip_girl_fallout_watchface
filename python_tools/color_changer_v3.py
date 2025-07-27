"""Changes color of all pixels, but saving transparency and brightness"""


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

                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                scaled_alpha = (a * brightness) // 255
                pixels[x, y] = (*new_color, scaled_alpha)

        im.save(image_path)


def process_folder(folder_path, new_color=(8, 230, 189)):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                image_path = os.path.join(root, file)
                print(f"Processing: {image_path}")
                recolor_grayscale_to_transparent(image_path, new_color)


if __name__ == "__main__":
    target_folder = r"C:\Users\DY\PycharmProjects\mi_band_9_pro_pip_girl_fallout_watchface\media_src\converter_2"
    blue             = (8, 141, 230)
    gray             = (222, 222, 222)
    ninja_gray       = (127, 127, 127)
    yellow           = (255, 237, 0)
    orange           = (255, 80, 0)
    fux              = (169, 0, 255)
    blueberry_yogurt = (186, 139, 239)
    meadow_green     = (152, 215, 105)
    ocean_blue       = (0, 203, 255)
    armor_green      = (105, 215, 105)
    shameless_red    = (224, 110, 101)
    toxic_green      = (151, 225, 61)
    process_folder(target_folder, toxic_green)
