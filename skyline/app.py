from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from widgets.location import Location
from widgets.weather import Weather
from services.weather_api import get_weather


class WeatherApp(App):
    TITLE = "Skyline"
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("r", "reset", "New search"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Location()
        yield Footer()

    async def on_location_location_submitted(self, message: Location.LocationSubmitted) -> None:
        location_widget = self.query_one(Location)
        location_widget.remove()

        weather_widget = Weather(message.location)
        self.mount(weather_widget)

        try:
            data = await get_weather(message.location)
            weather_widget.display_weather(data)
        except Exception as e:
            weather_widget.display_error(str(e))

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_reset(self) -> None:
        weather = self.query("Weather")
        for w in weather:
            w.remove()
        self.mount(Location())


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
