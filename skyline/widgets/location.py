from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Label, Input


class Location(Widget):

    def compose(self) -> ComposeResult:
        with Container(id="container"):
            yield Label("Location", id="title")
            yield Input("location", id="location")
