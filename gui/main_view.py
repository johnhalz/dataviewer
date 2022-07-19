from sys import platform
from plyer import filechooser

from .selector_view import SelectorView
from .metadata_view import MetadataView
from .data_view import DataView

import dearpygui.dearpygui as dpg

from sys import path
from os.path import dirname, join, abspath
path.insert(0, abspath(join(dirname(__file__), '..')))

from data_handler.data_handler import DataHandler

def screen_size():
    from screeninfo import get_monitors
    from os import environ
    
    environ['DISPLAY'] = ':0.0'
    screen = get_monitors()[0]

    return screen.width, screen.height

def open_file_dialog(data: DataHandler):
    if platform == 'win32':
        files = filechooser.open_file(multiple=True)
    
    data.add_files(files)

def main_view():

    dpg.create_context()


    with dpg.window(label='MainWindow', tag='MainWindow', no_background=True) as main_window:
        SelectorView()
        MetadataView()
        DataView()

    data_handler = DataHandler()

    screen_width, screen_height = screen_size()
    screen_ratio = [0.5, 0.65]

    dpg.create_viewport(title='H5 Viewer',
                        width=int(screen_width*screen_ratio[0]),
                        height=int(screen_height*screen_ratio[1]),
                        x_pos=int(screen_width*((1-screen_ratio[0])/2)),
                        y_pos=int(screen_height*((1-screen_ratio[1])/2)))

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open...", callback=lambda: open_file_dialog(data_handler))

        with dpg.menu(label="Developer", tag='developer_menu', show=False):
            dpg.add_menu_item(label="Save Init File", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))
            dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_metrics())
            dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_font_manager())

        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About")
            dpg.add_menu_item(label="Show Developer Options", tag='show_dev_button', show=True, callback=lambda: dpg.show_item(item='developer_menu'))
            dpg.add_menu_item(label="Hide Developer Options", tag='hide_dev_button', show=True, callback=lambda: dpg.hide_item(item='developer_menu'))

    dpg.configure_app(docking=True, docking_space=True, init_file="config/custom_gui_layout.ini", load_init_file=True)
    dpg.setup_dearpygui()
    dpg.set_primary_window(main_window, True) # Fill viewport
    
    
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

