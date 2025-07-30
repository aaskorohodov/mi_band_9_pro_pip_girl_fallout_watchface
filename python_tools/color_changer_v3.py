"""Changes color of all pixels, but saving transparency and brightness"""


import os

from PIL import Image


def recolor_image(image_path: str,
                  new_color: tuple[int, int, int]) -> None:
    """Changes color of an image. Replaces image

    Args:
        image_path: Path to image to change color of
        new_color: Tuple with RGB-color"""

    with Image.open(image_path).convert("RGBA") as im:
        pixels = im.load()
        width, height = im.size

        for y in range(height):
            for x in range(width):
                r, g, b, alpha = pixels[x, y]

                # skip fully transparent
                pixel_is_transparent = alpha == 0
                if pixel_is_transparent:
                    continue

                brightness = (r + g + b) / (3 * 255)
                new_r = int(new_color[0] * brightness)
                new_g = int(new_color[1] * brightness)
                new_b = int(new_color[2] * brightness)

                pixels[x, y] = (new_r, new_g, new_b, alpha)

        im.save(image_path)


def check_extension(file_name: str,
                    extensions: list[str]) -> bool:
    """Checks if file has specific extension

    Args:
        file_name: Name of the file to check
        extensions: List with extensions to check file_name for
    Returns:
        True, if file_name has provided extension"""

    for extension in extensions:
        if file_name.endswith(extension):
            return True
    return False


def process_folder(folder_path: str,
                   new_color: tuple[int, int, int]) -> None:
    """Processes images in a folder and changes their color

    Notes:
        Converts only .PNG
    Args:
        folder_path: Path to the folder with images
        new_color: Tuple with RGB-color, to convert all images into"""

    convert_these_extensions = ['.png']

    for root, _, files in os.walk(folder_path):
        for file in files:
            if check_extension(file, convert_these_extensions):
                image_path = os.path.join(root, file)
                print(f"Processing: {image_path}")
                recolor_image(image_path, new_color)


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
    monroe_yellow    = (248, 188, 90)
    velma_orange     = (252, 140, 81)

    process_folder(target_folder, velma_orange)
