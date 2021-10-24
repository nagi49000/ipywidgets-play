import ipywidgets
from unittest.mock import patch
from traitlets.traitlets import TraitError
from pytest import raises


def mock_interact(*args, **kwargs):
    """ create a mock for the interact decorator, a la
        https://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function

        Need to create mock and directly patch BEFORE importing the objects-under-test
    """
    f = args[0]  # assume first arg is function
    f()  # just call the function, mimicing the widget 'appearing' in jupyter


patch('ipywidgets.interact', mock_interact).start()

# can now import the objects-under-test, with the library patched
import simple_widgets  # noqa


def test_simple_widgets_default_values(monkeypatch):
    # as we interact with the instance more widgets appear

    s = simple_widgets.SimpleWidgets()
    assert s._int_slider_widget is None
    assert s._clicked_next_widget is None
    assert s._button is None
    assert s.last_value is None

    s.run_simple_widgets()
    assert isinstance(s._int_slider_widget, ipywidgets.IntSlider)
    assert s._clicked_next_widget is None
    assert isinstance(s._button, ipywidgets.Button)
    assert s.last_value is None

    s._button.click()
    assert isinstance(s._int_slider_widget, ipywidgets.IntSlider)
    assert isinstance(s._clicked_next_widget, ipywidgets.Dropdown)
    assert isinstance(s._button, ipywidgets.Button)
    assert s.last_value == "alpha"


def test_simple_widgets_to_dropdown(monkeypatch):
    s = simple_widgets.SimpleWidgets()
    s.run_simple_widgets()

    # should get a dropdown for this value
    s._int_slider_widget.value = 12
    assert s._int_slider_widget.value == 12
    s._button.click()
    assert s.last_value == "alpha"

    # check effect of setting dropdown value
    with raises(TraitError):
        s._clicked_next_widget.value = "i am not a valid value"
    assert s.last_value == "alpha"

    s._clicked_next_widget.value = "gamma"
    assert s.last_value == "gamma"


def test_simple_widgets_to_checkbox(monkeypatch):
    s = simple_widgets.SimpleWidgets()
    s.run_simple_widgets()

    # should get a checkbox for this value
    s._int_slider_widget.value = 9
    assert s._int_slider_widget.value == 9
    s._button.click()
    assert isinstance(s._clicked_next_widget, ipywidgets.Checkbox)
    assert s.last_value is False

    s._clicked_next_widget.value = True
    assert s.last_value is True


def test_simple_widgets_changing_slider_value(monkeypatch):
    s = simple_widgets.SimpleWidgets()
    s.run_simple_widgets()
    s._int_slider_widget.value = 12
    s._button.click()

    assert isinstance(s._clicked_next_widget, ipywidgets.Dropdown)
    assert s.last_value == "alpha"

    s._int_slider_widget.value = 8
    assert isinstance(s._clicked_next_widget, ipywidgets.Dropdown)
    s._button.click()  # should change the lower widget

    assert isinstance(s._clicked_next_widget, ipywidgets.Checkbox)
    assert s.last_value is False
    s._clicked_next_widget.value = True
    assert s.last_value is True

    s._button.click()  # should renew the Checkbox
    assert isinstance(s._clicked_next_widget, ipywidgets.Checkbox)
    assert s.last_value is False

    s._int_slider_widget.value = 20
    assert isinstance(s._clicked_next_widget, ipywidgets.Checkbox)
    s._button.click()  # should change the lower widget
    assert isinstance(s._clicked_next_widget, ipywidgets.Dropdown)
    assert s.last_value == "alpha"

    s._clicked_next_widget.value = "beta"
    assert s.last_value == "beta"

    s._int_slider_widget.value = 25
    s._button.click()  # should reset the lower widget
    assert isinstance(s._clicked_next_widget, ipywidgets.Dropdown)
    assert s.last_value == "alpha"
