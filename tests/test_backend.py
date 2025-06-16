from unittest.mock import MagicMock
from finance_app.backend import backend


def test_get_date_range_day():
    app = MagicMock()
    app.date_filter = "day"
    start, end = backend.get_date_range(app)
    assert start == end


def test_set_filter_triggers_refresh():
    app = MagicMock()
    backend.set_filter(app, "month")
    app.refresh_view.assert_called_once()
    assert app.date_filter == "month"
