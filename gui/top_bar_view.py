from dearpygui import dearpygui as dpg
import plyer
from general_util.file import File

class TopBarView:

    def __init__(self) -> None:
        # Define default parameters
        self.file_paths = ''

        self.test_manager = dpg.generate_uuid()
        self.view()

    def open_file_explorer(self):
        self.file_paths = plyer.filechooser.open_file()

    def view(self):
        with dpg.window(label="Test Manager",
                        no_collapse=True,
                        no_title_bar=False,
                        no_close=True,
                        height=10,
                        tag=self.test_manager):

            with dpg.group(horizontal=True):
                dpg.add_button(label="Open File...", callback=self.open_file_explorer)
                dpg.add_input_text(default_value='', tag='file_path', hint='Enter file path here')
                dpg.add_button(label="Save Init", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))