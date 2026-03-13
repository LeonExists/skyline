from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Label, Input
from textual.message import Message


class Location(Widget):

    class LocationSubmitted(Message):
        def __init__(self, location: str):
            self.location = location
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Location", id="title")
        yield Input(placeholder="New York", id="location")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        location = event.value.strip()
        if location:
            self.post_message(self.LocationSubmitted(location))
