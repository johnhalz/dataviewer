from dearpygui import dearpygui as dpg

from data_handler.data_handler import DataHandler

class SelectorView:
    def __init__(self, data_handler: DataHandler) -> None:
        self.selector_view = dpg.generate_uuid()
        self.tag = 'selector_view'
        self.data_handler = data_handler
        self.view()


    def view(self):
        with dpg.window(label="Selector Tree", tag=self.tag, autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_input_text(tag='tree_search', hint='Search', width=-1)
            dpg.add_button(label="No Files Opened", width=-1, height=-1, enabled=False, show=len(self.data_handler.file_list) == 0)
            dpg.add_tree_node(label='(Files go here)', show=len(self.data_handler.file_list) != 0)
