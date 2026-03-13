from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from widgets.location import Location
from widgets.weather import Weather


class WeatherApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]


    def compose(self) -> ComposeResult:
        yield Header()

        yield Location()

        yield Footer()


    def on_location_location_submitted(self, message: Location.LocationSubmitted) -> None:
        # remove location widget
        location_widget = self.query_one(Location)
        location_widget.remove()

        # mount weather widget with the submitted location
        self.mount(Weather(message.location))


    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )



if __name__ == "__main__":
    app = WeatherApp()
    app.run()