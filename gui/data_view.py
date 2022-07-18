from dearpygui import dearpygui as dpg

class DataView:
    def __init__(self) -> None:
        self.data_view = dpg.generate_uuid()
        self.view()

    def view(self):
        with dpg.window(label="Data View", width=400, height=400, tag="data_view", autosize=True):
            dpg.add_text("There should be a table view here.")