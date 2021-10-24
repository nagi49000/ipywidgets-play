from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display


class SimpleWidgets():
    def __init__(self):
        self._int_slider_widget = None
        self._clicked_next_widget = None
        self._button = None

    def do_stuff_on_click(self, b):
        if self._clicked_next_widget:
            self._clicked_next_widget.close()
        if self._int_slider_widget.value < 10:
            @interact
            def get_check_box():
                x = widgets.Checkbox(value=False, description='Check me')
                self._clicked_next_widget = x
                return x
        else:
            @interact
            def get_text():
                x = widgets.Dropdown(options=['alpha', 'beta', 'gamma'], value='alpha', description='Text:')
                self._clicked_next_widget = x
                return x

    def run_simple_widgets(self):

        @interact
        def get_int_slider():
            x = widgets.IntSlider(min=0, max=30, step=1, value=10)
            self._int_slider_widget = x
            return x

        self._button = widgets.Button(description="Click Me!")
        display(self._button)
        self._button.on_click(self.do_stuff_on_click)

    @property
    def last_value(self):
        if self._clicked_next_widget:
            return self._clicked_next_widget.value
        else:
            return None
