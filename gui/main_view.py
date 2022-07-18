from .selector_view import SelectorView
from .metadata_view import MetadataView
from .data_view import DataView

def screen_size():
    from screeninfo import get_monitors
    from os import environ
    
    environ['DISPLAY'] = ':0.0'
    screen = get_monitors()[0]

    return screen.width, screen.height

def main_view():
    import dearpygui.dearpygui as dpg

    dpg.create_context()

    with dpg.window(label='MainWindow', tag='MainWindow', no_background=True) as main_window:
        SelectorView()
        MetadataView()
        DataView()


    screen_width, screen_height = screen_size()
    screen_ratio = [0.5, 0.65]

    dpg.create_viewport(title='H5 Viewer',
                        width=int(screen_width*screen_ratio[0]),
                        height=int(screen_height*screen_ratio[1]),
                        x_pos=int(screen_width*((1-screen_ratio[0])/2)),
                        y_pos=int(screen_height*((1-screen_ratio[1])/2)))

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open...")
            dpg.add_menu_item(label="Save As")

        with dpg.menu(label="Developer"):
            dpg.add_menu_item(label="Save Init File")

        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About")
            dpg.add_menu_item(label="Show Developer Options")

    dpg.configure_app(docking=True, docking_space=True)
    dpg.setup_dearpygui()
    dpg.set_primary_window(main_window, True) # Fill viewport
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

