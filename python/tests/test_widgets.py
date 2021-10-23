from widgets import SimpleWidgets


def test_simple_widgets():
    s = SimpleWidgets()
    assert s._int_slider_widget is None
    assert s._clicked_next_widget is None
    assert s._button is None
    assert s.last_value is None

    s.run_simple_widgets()
    assert s._button is not None
    assert s.last_value is None
    assert s._int_slider_widget is None  # this is wrong
