from dearpygui import dearpygui as dpg

class SelectorView:
    def __init__(self) -> None:
        self.selector_view = dpg.generate_uuid()
        self.tag = 'selector_view'
        self.view()


    def view(self):
        with dpg.window(label="Selector Tree", tag=self.tag, autosize=True, no_close=True, no_collapse=True, no_move=True):
            dpg.add_input_text(tag='tree_search', hint='Search', width=-1)
            dpg.add_tree_node(label='(Files go here)')
