import dearpygui.dearpygui as dpg

class AboutView:
    def __init__(self) -> None:
        self.tag = 'about_view'
        self.view()


    def view(self):
        with dpg.window(label="About", modal=True, show=False, tag=self.tag):
            dpg.add_text("Name: H5 Viewer")
            dpg.add_text('Author: John Halazonetis (john.halazonetis@icloud.com)')
