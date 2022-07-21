from dearpygui import dearpygui as dpg

class MetadataView:
    def __init__(self) -> None:
        self.metadata_view = dpg.generate_uuid()
        self.tag = 'metadata_view'
        self.view()


    def view(self):
        with dpg.window(label="Metadata View", tag=self.tag, autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_button(label="No File Selected", width=-1, height=-1, enabled=False)
