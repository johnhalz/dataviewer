from .topbar_view import TopBarView

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
        TopBarView()


    screen_width, screen_height = screen_size()
    screen_ratio = [0.5, 0.65]

    dpg.create_viewport(title='H5 Viewer',
                        width=int(screen_width*screen_ratio[0]),
                        height=int(screen_height*screen_ratio[1]),
                        x_pos=int(screen_width*((1-screen_ratio[0])/2)),
                        y_pos=int(screen_height*((1-screen_ratio[1])/2)))
    dpg.setup_dearpygui()
    dpg.set_primary_window(main_window, True) # Fill viewport
    dpg.show_viewport()
    dpg.configure_app(docking=True)
    dpg.start_dearpygui()
    dpg.destroy_context()

