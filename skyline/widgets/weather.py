from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Sparkline
from textual.containers import Horizontal, Vertical


class Weather(Widget):
    def __init__(self, location: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="main-weather") as main:
                main.border_title = f"[bold]{self.location}[/bold]"
                yield Label("72°F", id="temperature")
                yield Label("Partly Cloudy", id="conditions")

            with Vertical(id="weather-details"):
                with Vertical(id="details-top") as top:
                    top.border_title = "Details"

                with Vertical(id="details-bottom") as bottom:
                    bottom.border_title = "7-Day Forecast"
