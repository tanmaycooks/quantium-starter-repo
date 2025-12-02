from dash.testing.application_runners import import_app
from dash import html

def test_header_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", "Pink Morsel Sales Dashboard", timeout=10)
    assert dash_duo.find_element("h1").text == "Pink Morsel Sales Dashboard"

def test_visualization_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#time-series-chart", timeout=10)
    assert dash_duo.find_element("#time-series-chart")

def test_region_picker_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    assert dash_duo.find_element("#region-filter")
