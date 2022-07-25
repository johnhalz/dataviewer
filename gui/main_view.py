import os
from general_util import FileDialog, File

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

        self._make_centered_text_possible()
        
        with dpg.window(label='MainWindow', tag='main_window', no_background=True) as main_window:
            self.selectorview = SelectorView()
            self.metdataview = MetadataView()
            self.dataview = DataView()
            self.aboutview = AboutView()

        screen_width, screen_height = self._screen_size()
        self._update_tree_view()

        dpg.create_viewport(title='H5 Viewer',
                            width=int(screen_width*self.screen_ratio[0]),
                            height=int(screen_height*self.screen_ratio[1]),
                            x_pos=int(screen_width*((1-self.screen_ratio[0])/2)),
                            y_pos=int(screen_height*((1-self.screen_ratio[1])/2)))

        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open Files...", callback=self._open_file, shortcut="Ctrl O")
                dpg.add_menu_item(label="Open Folder...", callback=self._open_folder, shortcut="Ctrl Shift O")
                with dpg.menu(label='Open Recent'):
                    dpg.add_menu_item(label="(None)", enabled=False)

            with dpg.menu(label="Developer", tag='developer_menu', show=self.dev_mode):
                dpg.add_menu_item(label="Save Init File", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))
                dpg.add_menu_item(label="Show About", callback=lambda:dpg.show_tool(dpg.mvTool_About))
                dpg.add_menu_item(label="Show Metrics", callback=dpg.show_metrics)
                dpg.add_menu_item(label="Show Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
                dpg.add_menu_item(label="Show Debug", callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
                dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
                dpg.add_menu_item(label="Show Font Manager", callback=dpg.show_font_manager)
                dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
                dpg.add_separator()
                dpg.add_menu_item(label="Dark Theme (default)")
                dpg.add_menu_item(label="Light Theme")

            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=lambda: dpg.configure_item(item='about_view', show=True))
                dpg.add_menu_item(label="Show Developer Options", tag='show_dev_button', show=not self.dev_mode, callback=self._toggle_dev_mode)
                dpg.add_menu_item(label="Hide Developer Options", tag='hide_dev_button', show=self.dev_mode, callback=self._toggle_dev_mode)

        dpg.configure_app(docking=True, docking_space=True, init_file="config/custom_gui_layout.ini", load_init_file=True)
        dpg.setup_dearpygui()
        dpg.set_primary_window(main_window, True) # Fill viewport
        
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


    def _toggle_dev_mode(self):
        # Update dev mode variable
        self.dev_mode = not self.dev_mode

        # Configure windows in app
        dpg.configure_item(item=self.selectorview.tag, no_move=not self.dev_mode, autosize=not self.dev_mode, no_collapse=not self.dev_mode)
        dpg.configure_item(item=self.metdataview.tag, no_move=not self.dev_mode, autosize=not self.dev_mode, no_collapse=not self.dev_mode)
        dpg.configure_item(item=self.dataview.tag, no_move=not self.dev_mode, autosize=not self.dev_mode, no_collapse=not self.dev_mode)

        # Update menu bar
        dpg.configure_item(item='developer_menu', show=self.dev_mode)
        dpg.configure_item(item='show_dev_button', show=not self.dev_mode)
        dpg.configure_item(item='hide_dev_button', show=self.dev_mode)

    
    def _screen_size(self):
        from screeninfo import get_monitors
        from os import environ
        
        environ['DISPLAY'] = ':0.0'
        screen = get_monitors()[0]

        return screen.width, screen.height


    def _open_file(self):
        file_dialog = FileDialog()
        files = file_dialog.open_file()
        self.data_handler.add_files(files)
        self._update_tree_view()


    def _open_folder(self):
        file_dialog = FileDialog()
        directory = file_dialog.open_dir()

        # Loop through h5 files in folder
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                # Only handle h5 files
                if File.get_file_extension(file) == '.h5':
                    file_paths.append(os.path.join(root, file))     # Get full path
        
        self.data_handler.add_files(file_paths)
        self._update_tree_view()
        
    
    def _make_centered_text_possible(self):
        """
        Make a disabled button act as centered text
        """
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [0, 0, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
        dpg.bind_theme(global_theme)


    def _update_tree_view(self):
        # If there are no files in the file list
        if self.data_handler.files == {}:
            dpg.show_item(item='sv_no_files')
            dpg.disable_item(item='tree_search')

        # If there are files present in the file list
        else:
            dpg.hide_item(item='sv_no_files')
            dpg.enable_item(item='tree_search')

            for file in self.data_handler.newly_added_files.keys():
                file_node = dpg.add_tree_node(label=File.only_filename(input_path=str(file)),
                                              parent=self.selectorview.tag,
                                              selectable=True)

                for group in self.data_handler.newly_added_files[file].keys():
                    group_node = dpg.add_tree_node(label=group,
                                                   parent=file_node,
                                                   selectable=True)

                    for table in self.data_handler.newly_added_files[file][group].keys():
                        tag = f'{File.only_filename(input_path=str(file), with_extension=False)}/{group}/{table}'
                        table_node = dpg.add_selectable(label=table,
                                                       parent=group_node,
                                                       callback=lambda: print(self.data_handler.files[file][group][table].attrs))
