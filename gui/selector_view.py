from dearpygui import dearpygui as dpg

class SelectorView:
    def __init__(self) -> None:
        self.selector_view = dpg.generate_uuid()
        self.view()

    def view(self):
        with dpg.window(label="Selector Tree", tag="selector_view", autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_tree_node(label="tree node")
            dpg.add_input_text(tag='tree_search', hint='Search')
