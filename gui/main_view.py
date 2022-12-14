import os
from general_util import File, FileDialog

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
        self.data_handler = data_handler
        self.recent_files_log = 'config/recent_files.txt'

        self.view()


    def view(self):

        self.file_manager = FileDialog()
        dpg.create_context()

        self._make_centered_text_possible()
        
        with dpg.window(label='MainWindow', tag='main_window', no_background=True) as main_window:
            self.selectorview = SelectorView()
            self.metdataview = MetadataView()
            self.dataview = DataView()
            self.aboutview = AboutView()

        self._update_tree_view()

        window_width, window_height, window_xpos, window_ypos = self._window_size(ratio=[0.5, 0.65])

        dpg.create_viewport(title='H5 Viewer', width=window_width, height=window_height, x_pos=window_xpos, y_pos=window_ypos)

        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open...", callback=self._open_file, shortcut="Ctrl O")
                dpg.add_menu(label='Open Recent', tag='recent_files_menu_item')
                    # dpg.add_menu_item(label="(None)", enabled=False, tag='no_recent_files_menu_item')

                dpg.add_separator()
                dpg.add_menu_item(label="Preferences")

            with dpg.menu(label="Developer", tag='developer_menu', show=self.dev_mode):
                dpg.add_menu_item(label="Save Init File", callback=lambda: dpg.save_init_file("config/custom_gui_layout.ini"))
                dpg.add_menu_item(label="Show About", callback=lambda:dpg.show_tool(dpg.mvTool_About))
                dpg.add_menu_item(label="Show Metrics", callback=dpg.show_metrics)
                dpg.add_menu_item(label="Show Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
                dpg.add_menu_item(label="Show Debug", callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
                dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
                dpg.add_menu_item(label="Show Font Manager", callback=dpg.show_font_manager)
                dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))

            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=lambda: dpg.configure_item(item='about_view', show=True))
                dpg.add_menu_item(label="Show Developer Options", tag='show_dev_button', show=not self.dev_mode, callback=self._toggle_dev_mode)
                dpg.add_menu_item(label="Hide Developer Options", tag='hide_dev_button', show=self.dev_mode, callback=self._toggle_dev_mode)

        self._load_recent_files()
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


    def _window_size(self, ratio: list, placement: str = 'center'):
        from screeninfo import get_monitors
        from os import environ
        
        environ['DISPLAY'] = ':0.0'
        screen = get_monitors()[0]

        window_width = int(screen.width * ratio[0])
        window_height = int(screen.height * ratio[1])

        if placement == 'center':
            window_xpos = int(screen.width * ((1-ratio[0])/2) )
            window_ypos = int(screen.height * ((1-ratio[1])/2) )
        else:
            if 'top' in placement:
                window_ypos = 0
            elif 'bottom' in placement:
                window_ypos = screen.height - window_height

            if 'left' in placement:
                window_xpos = 0
            elif 'right' in placement:
                window_xpos = screen.width - window_width

        return window_width, window_height, window_xpos, window_ypos
        
    
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


    def _open_file(self):
        from sys import platform
        if platform != 'darwin':
            files = self.file_manager.open_file()
            self._open_and_update(files)

        else:
            window_width, window_height, _, _ = self._window_size(ratio=[0.4, 0.5])
            with dpg.file_dialog(label='Choose File or Folder...',
                                width=window_width,
                                height=window_height,
                                modal=True, callback=lambda _, a, __ : self._open_and_update(list(a['selections'].values()))):
                dpg.add_file_extension(".h5", color=(255, 255, 255, 255))
    

    def _open_and_update(self, files):
        if isinstance(files, str):
            files = [files]

        self.data_handler.add_files(files)
        self._update_tree_view()
        self._save_to_open_recent(files)


    def _save_to_open_recent(self, files):
        if not File.path_exists(self.recent_files_log):
            with open(self.recent_files_log, 'w') as f:
                f.write('\n'.join(files))

        else:
            with open(self.recent_files_log, 'a') as f:
                # TODO: Check that file is not already in txt file (if yes, move to bottom of txt file)
                f.writelines('\n'.join(files))


    def _load_recent_files(self):
        if not File.path_exists(self.recent_files_log):
            dpg.add_menu_item(label="(None)", enabled=False, tag='no_recent_files_menu_item', parent='recent_files_menu_item')
        else:
            with open(self.recent_files_log, 'r') as f:
                lines = f.readlines()

                if len(lines) == 0:
                    dpg.add_menu_item(label="(None)", enabled=False, tag='no_recent_files_menu_item', parent='recent_files_menu_item')
                else:
                    # Most recently opened file is at bottom of list
                    for file in reversed(lines):
                        dpg.add_menu_item(label=file, parent='recent_files_menu_item', callback=lambda: self._open_and_update(file))



    # TODO: Integrate with normal open operation
    def _open_folder(self):
        directory = self.file_manager.open_dir()

        # Loop through h5 files in folder
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                # Only handle h5 files
                if File.get_file_extension(file) == '.h5':
                    file_paths.append(os.path.join(root, file))     # Get full path
        
        self.data_handler.add_files(file_paths)
        self._update_tree_view()


    def _update_tree_view(self):
        # If there are no files in the file list
        if self.data_handler.files == {}:
            dpg.show_item(item='sv_no_files')
            dpg.configure_item(item='tree_search', show=False)

        # If there are files present in the file list
        else:
            dpg.hide_item(item='sv_no_files')
            dpg.configure_item(item='tree_search', show=True)

            for file in self.data_handler.newly_added_files.keys():
                print(file)
                file_node = dpg.add_tree_node(label=File.only_filename(input_path=str(file)),
                                              parent=self.selectorview.tag,
                                              selectable=True)

                for group in self.data_handler.newly_added_files[file].keys():
                    group_node = dpg.add_tree_node(label=group,
                                                   parent=file_node,
                                                   selectable=True)

                    for table in self.data_handler.newly_added_files[file][group].keys():
                        dpg.add_selectable(label=table,
                                           parent=group_node,
                                           callback=lambda: print(self.data_handler.files[file][group][table].attrs))
