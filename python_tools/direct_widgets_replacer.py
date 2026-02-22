"""Replaces exact widgets with updated version. Automatically searches for .fprj files"""


import os
import shutil
from datetime import datetime


class WidgetSpecificUpdater:
    def __init__(self, updates_map: dict):
        """
        :param updates_map: A dictionary where { "old_string": "new_string" }
        """
        self.updates_map = updates_map

    def back_up_file(self, target_path: str) -> None:
        reserve_dir = os.path.join(os.path.dirname(target_path), 'reserve')
        os.makedirs(reserve_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(reserve_dir, f'{os.path.basename(target_path)}.backup_{timestamp}')
        shutil.copy2(target_path, backup_path)

    def update_target_file(self, target_path: str):
        with open(target_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        changed = False
        new_lines = []

        for line in lines:
            stripped_line = line.strip()
            # Check if this line is one of our targets
            if stripped_line in self.updates_map:
                indent = line[:line.find('<')]  # Preserve original indentation
                new_line = indent + self.updates_map[stripped_line] + '\n'
                new_lines.append(new_line)
                changed = True
            else:
                new_lines.append(line)

        if changed:
            self.back_up_file(target_path)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Successfully updated: {target_path}")
        else:
            print(f"No matching widgets found in: {target_path}")

    def is_valid_target(self, file_path: str) -> bool:
        is_desired_file = file_path.endswith('.fprj') and os.path.basename(file_path).startswith('PipGirlProject')
        not_reserver = 'reserve' not in file_path
        return is_desired_file and not_reserver

    def process_files(self, find_files_here_path: str) -> None:
        for dirpath, _, filenames in os.walk(find_files_here_path):
            for filename in filenames:
                target_path = os.path.join(dirpath, filename)
                if self.is_valid_target(target_path):
                    self.update_target_file(target_path)


if __name__ == '__main__':
    # Define your mapping here
    # TIP: Copy the EXACT line from the .fprj file (the one you want to replace)
    MAPPING = {
        '<Widget Shape="31" Name="warn_weather" BitmapList="(-30):warn_cold_3.png|(-25):warn_cold_2.png|(-15):warn_cold_1.png|(-14):warn_weather_empty.png|(-4):warn_weather_empty.png|(-3):warn_cold_2.png|(2):warn_cold_2.png|(3):warn_weather_empty.png|(24):warn_weather_empty.png|(25):warn_hot_1.png|(28):warn_hot_2.png|(32):warn_hot_3.png" X="261" Y="368" Width="48" Height="48" Alpha="255" Alignment="0" DefaultIndex="0" Value_Src="0" Spacing="0" Blanking="0" Visible_Src="0" Index_Src="2031"/>':
        '<Widget Shape="31" Name="warn_weather" BitmapList="(-30):warn_cold_3.png|(-25):warn_cold_2.png|(-15):warn_cold_1.png|(-14):warn_weather_empty.png|(-4):warn_weather_empty.png|(-3):warn_cold_2.png|(2):warn_cold_2.png|(3):warn_weather_empty.png|(24):warn_weather_empty.png|(25):warn_hot_1.png|(28):warn_hot_2.png|(32):warn_hot_3.png" X="250" Y="368" Width="48" Height="48" Alpha="255" Alignment="0" DefaultIndex="0" Value_Src="0" Spacing="0" Blanking="0" Visible_Src="0" Index_Src="2031"/>',

        '<Widget Shape="32" Name="weather_temp_max" BitmapList="0_18.png|1_18.png|2_18.png|3_18.png|4_18.png|5_18.png|6_18.png|7_18.png|8_18.png|9_18.png|minus_18.png" X="306" Y="359" Width="48" Height="48" Alpha="255" Visible_Src="0" Digits="2" Alignment="2" Value_Src="1832" Spacing="0" Blanking="1"/>':
        '<Widget Shape="32" Name="weather_temp_max" BitmapList="0_18.png|1_18.png|2_18.png|3_18.png|4_18.png|5_18.png|6_18.png|7_18.png|8_18.png|9_18.png|minus_18.png" X="294" Y="359" Width="48" Height="48" Alpha="255" Visible_Src="0" Digits="3" Alignment="2" Value_Src="1832" Spacing="0" Blanking="1"/>',

        '<Widget Shape="32" Name="weather_temp_min" BitmapList="0_18.png|1_18.png|2_18.png|3_18.png|4_18.png|5_18.png|6_18.png|7_18.png|8_18.png|9_18.png|minus_18.png" X="305" Y="398" Width="48" Height="48" Alpha="255" Visible_Src="0" Digits="2" Alignment="2" Value_Src="2032" Spacing="0" Blanking="1"/>':
        '<Widget Shape="32" Name="weather_temp_min" BitmapList="0_18.png|1_18.png|2_18.png|3_18.png|4_18.png|5_18.png|6_18.png|7_18.png|8_18.png|9_18.png|minus_18.png" X="294" Y="398" Width="48" Height="48" Alpha="255" Visible_Src="0" Digits="3" Alignment="2" Value_Src="2032" Spacing="0" Blanking="1"/>'
    }

    folder_path = 'C:/Users/DY/PycharmProjects/mi_band_9_pro_pip_girl_fallout_watchface/watchfaces_src'

    updater = WidgetSpecificUpdater(MAPPING)
    updater.process_files(folder_path)
