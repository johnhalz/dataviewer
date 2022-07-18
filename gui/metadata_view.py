from dearpygui import dearpygui as dpg

class MetadataView:
    def __init__(self) -> None:
        self.metadata_view = dpg.generate_uuid()
        self.view()

    def view(self):
        with dpg.window(label="Metadata View", width=400, height=400, tag="metadata_view", autosize=True):
            dpg.add_text("There should be a list of different values here")