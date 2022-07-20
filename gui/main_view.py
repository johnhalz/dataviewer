from sys import platform

from .selector_view import SelectorView
from .metadata_view import MetadataView
from .data_view import DataView
from .about_view import AboutView

import dearpygui.dearpygui as dpg

from sys import path
from os.path import dirname, join, abspath
path.insert(0, abspath(join(dirname(__file__), '..')))

from data_handler.data_handler import DataHandler


class MainView:
    def __init__(self, data_handler: DataHandler) -> None:
        self.dev_mode: bool = False
        self.screen_ratio = [0.5, 0.65]
        self.data_handler = data_handler

        self.view()


    def view(self):

        dpg.create_context()
        
        with dpg.window(label='MainWindow', tag='main_window', no_background=True) as main_window:
            SelectorView()
            MetadataView()
            DataView()
            AboutView()

        screen_width, screen_height = self._screen_size()

        dpg.create_viewport(title='H5 Viewer',
                            width=int(screen_width*self.screen_ratio[0]),
                            height=int(screen_height*self.screen_ratio[1]),
                            x_pos=int(screen_width*((1-self.screen_ratio[0])/2)),
                            y_pos=int(screen_height*((1-self.screen_ratio[1])/2)))

        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open...", callback=lambda: self._open_file_dialog(self.data_handler))

            with dpg.menu(label="Developer", tag='developer_menu', show=self.dev_mode):
                dpg.add_menu_item(label="Save Init File", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))
                dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_metrics())
                dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_font_manager())
                dpg.add_separator()
                dpg.add_menu_item(label="Dark Theme (default)")
                dpg.add_menu_item(label="Light Theme")


            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=lambda: dpg.configure_item(item='about_view', show=True))
                dpg.add_menu_item(label="Show Developer Options", tag='show_dev_button', show=not self.dev_mode, callback=lambda: self._toggle_dev_mode())
                dpg.add_menu_item(label="Hide Developer Options", tag='hide_dev_button', show=self.dev_mode, callback=lambda: self._toggle_dev_mode())

        dpg.configure_app(docking=True, docking_space=True, init_file="config/custom_gui_layout.ini", load_init_file=True)
        dpg.setup_dearpygui()
        dpg.set_primary_window(main_window, True) # Fill viewport
        
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


    def _toggle_dev_mode(self):
        # Update dev mode variable
        self.dev_mode = not self.dev_mode

        # Update menu bar
        if self.dev_mode:
            dpg.show_item(item='developer_menu')
            dpg.hide_item(item='show_dev_button')
            dpg.show_item(item='hide_dev_button')
        else:
            dpg.hide_item(item='developer_menu')
            dpg.show_item(item='show_dev_button')
            dpg.hide_item(item='hide_dev_button')

    
    def _screen_size(self):
        from screeninfo import get_monitors
        from os import environ
        
        environ['DISPLAY'] = ':0.0'
        screen = get_monitors()[0]

        return screen.width, screen.height


    def _open_file_dialog(self, data: DataHandler):
        
        # Windows
        if platform == 'win32' or platform == 'linux':
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            files = filedialog.askopenfilename()

        # macOS
        elif platform == 'darwin':
            pass
        
        data.add_files(files)
