from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class Weather(Widget):
    def __init__(self, location: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location

    def compose(self) -> ComposeResult:
        yield Label(f"Weather for: {self.location}", id="title")
        
        yield Label("Temperature: Loading...", id="temperature")
        yield Label("Conditions: Loading...", id="conditions")
