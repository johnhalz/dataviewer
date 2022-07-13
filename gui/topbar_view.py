from dearpygui import dearpygui as dpg
from sys import platform
from general_util.file import File

class TopBarView:

    def __init__(self) -> None:
        # Define default parameters
        self.file_paths = ''

        self.test_manager = dpg.generate_uuid()
        self.view()

    def open_file_explorer(self):
        if platform == 'win32':     # For Windows
            import os
            self.file_paths = os.startfile(File.home_dir())
            # TODO: Verify expected behaviour on Windows
        elif platform == 'darwin':  # For macOS
            import subprocess
            self.file_paths = subprocess.Popen(['open', str(File.home_dir())])
            # TODO: Debug behaviour on macOS
        elif platform == 'Linux':   # For Linux
            import subprocess
            self.file_paths = subprocess.Popen(['xdg-open',str(File.home_dir())])
            # TODO: Verify expected behaviour on Linux

        print(self.file_paths)


    def view(self):
        with dpg.child_window(label='Top', height=35, autosize_x=True, border=False) as tb_window:

            with dpg.group(horizontal=True, ):
                dpg.add_button(label="Open File...", callback=self.open_file_explorer)
                dpg.add_input_text(default_value='', tag='file_path', hint='Enter file path here')
                # dpg.add_button(label="Save Init", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))