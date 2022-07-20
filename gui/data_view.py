from dearpygui import dearpygui as dpg

class DataView:
    def __init__(self) -> None:
        self.data_view = dpg.generate_uuid()
        self.tag = 'data_view'
        self.view()


    def view(self):
        with dpg.window(label="Data View", tag=self.tag, autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_text("There should be a table view here.")
