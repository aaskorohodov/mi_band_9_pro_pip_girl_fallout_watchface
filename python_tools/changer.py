"""Applies changes from a single fprj (watchface project) to all other fprj files, with saving Id and Title

Use it, to apply changes to all other watchfaces with different colors"""


import os
import shutil
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET

from datetime import datetime


class OtherColorsProjectsUpdater:
    def back_up_file(self,
                     target_path: str) -> None:
        """"""

        reserve_dir = os.path.join(os.path.dirname(target_path), 'reserve')
        os.makedirs(reserve_dir,
                    exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(reserve_dir, f'{os.path.basename(target_path)}.backup_{timestamp}')
        shutil.copy2(target_path, backup_path)

    def update_target_file(self, source_path, target_path):
        # Parse source and target XMLs
        source_tree = ET.parse(source_path)
        source_root = source_tree.getroot()
        source_screen = source_root.find('Screen')

        target_tree = ET.parse(target_path)
        target_root = target_tree.getroot()
        target_screen = target_root.find('Screen')

        # Preserve Id and Title
        original_id_value = target_root.attrib.get('Id')
        original_title_value = target_screen.attrib.get('Title') if target_screen is not None else None

        # Check for static_girl or anim in target
        preserved_widget = None
        preserved_index = None
        has_static_girl = False

        for i, child in enumerate(target_screen):
            if child.tag != 'Widget':
                continue
            name = child.attrib.get('Name')
            if name == 'static_girl':
                preserved_widget = child
                has_static_girl = True
                break
            elif name == 'anim_[0@150]':
                preserved_widget = child
                preserved_index = i

        # Remove anim_[0@150] from source, always
        source_screen[:] = [
            w for w in source_screen
            if not (w.tag == 'Widget' and w.attrib.get('Name') == 'anim_[0@150]')
        ]

        # Replace everything in target with source
        target_root.clear()
        target_root.attrib = source_root.attrib.copy()
        for child in list(source_root):
            target_root.append(child)

        # Restore Id and Title
        target_root.attrib['Id'] = original_id_value
        new_screen = target_root.find('Screen')
        new_screen.attrib['Title'] = original_title_value

        # Reinsert preserved widget
        if preserved_widget is not None:
            if has_static_girl:
                new_screen.append(preserved_widget)  # static_girl always last
            else:
                new_screen.insert(preserved_index, preserved_widget)  # reinsert anim at original position

        # Backup and write
        self.back_up_file(target_path)
        ET.ElementTree(target_root).write(target_path,
                                          encoding='utf-8',
                                          xml_declaration=True)

    def is_valid_target(self,
                        file_path):
        if not file_path.endswith('.fprj'):
            return False
        if not os.path.basename(file_path).startswith('PipGirlProject'):
            return False

        parent_dir = os.path.dirname(file_path)
        return (
            os.path.isdir(os.path.join(parent_dir, 'images')) and
            os.path.isfile(os.path.join(parent_dir, 'preview_default_large.png'))
        )

    def process_files(self,
                      source_file_path: str,
                      find_files_here_path: str) -> None:
        """"""

        source_file_path = os.path.abspath(source_file_path)
        for dirpath, _, filenames in os.walk(find_files_here_path):
            for filename in filenames:
                if not filename.endswith('.fprj'):
                    continue
                target_path = os.path.join(dirpath, filename)
                if os.path.abspath(target_path) == source_file_path:
                    continue
                if self.is_valid_target(target_path):
                    print(f'Updating: {target_path}')
                    self.update_target_file(source_file_path, target_path)


if __name__ == '__main__':
    updated_from_path = \
        ('C:/Users/DY/PycharmProjects/mi_band_9_pro_pip_girl_fallout_watchface/watchfaces_src/PipGirlProject/Extra/'
         'PipGirlProject_standard.fprj')
    folder_to_find_files_in_path = 'C:/Users/DY/PycharmProjects/mi_band_9_pro_pip_girl_fallout_watchface/watchfaces_src'

    if not updated_from_path or not folder_to_find_files_in_path:
        raise AssertionError('Specify source_file_path and find_files_here_path!')

    updater = OtherColorsProjectsUpdater()
    updater.process_files(updated_from_path, folder_to_find_files_in_path)
