from dearpygui import dearpygui as dpg

class MetadataView:
    def __init__(self) -> None:
        self.metadata_view = dpg.generate_uuid()
        self.view()

    def view(self):
        with dpg.window(label="Metadata View", tag="metadata_view", autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_text("There should be a list of different values here")