from dearpygui import dearpygui as dpg
import plyer
from general_util import File

# TODO: Replace TopBarView with DPG menu bar
class TopBarView:

    def __init__(self) -> None:
        # Define default parameters
        self.file_path = ''

        self.test_manager = dpg.generate_uuid()
        self.view()


    def open_file_explorer(self):

        self.file_path = plyer.filechooser.open_file(multpile=True)

        # TODO: Check if file paths are h5 or not

        dpg.set_value(item='file_path_text', value=self.file_path)  # Update text field with new file path


    def view(self):
        with dpg.child_window(label='Top', height=35, autosize_x=True, border=False):

            with dpg.group(horizontal=True, ):
                dpg.add_button(label="Open...", callback=self.open_file_explorer)
                dpg.add_input_text(default_value='', tag='file_path_text', hint='Enter file path here')
