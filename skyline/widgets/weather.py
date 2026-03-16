from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Sparkline, LoadingIndicator
from textual.containers import Horizontal, Vertical
from textual.message import Message

from services.weather_api import WeatherData


DAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Weather(Widget):
    class WeatherLoaded(Message):
        def __init__(self, data: WeatherData):
            self.data = data
            super().__init__()

    class WeatherError(Message):
        def __init__(self, error: str):
            self.error = error
            super().__init__()

    def __init__(self, location: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.weather_data: WeatherData | None = None

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="main-weather") as main:
                main.border_title = f"[bold]{self.location}[/bold]"
                yield LoadingIndicator(id="loading")
                yield Label("", id="temperature")
                yield Label("", id="conditions")

            with Vertical(id="weather-details"):
                with Vertical(id="details-top") as top:
                    top.border_title = "Details"
                    yield Label("", id="detail-feels-like")
                    yield Label("", id="detail-humidity")
                    yield Label("", id="detail-wind")
                    yield Label("", id="detail-uv")
                    yield Label("", id="detail-precip")

                with Vertical(id="details-bottom") as bottom:
                    bottom.border_title = "7-Day Forecast"
                    yield Label("", id="forecast-text")

                with Vertical(id="details-sparkline") as spark:
                    spark.border_title = "24h Temperature"
                    yield Sparkline([], id="temp-sparkline")

    def display_weather(self, data: WeatherData) -> None:
        self.weather_data = data
        c = data.current

        self.query_one("#loading", LoadingIndicator).display = False

        main = self.query_one("#main-weather", Vertical)
        main.border_title = f"[bold]{data.location.name}, {data.location.country}[/bold]"

        self.query_one("#temperature", Label).update(f"{c.temperature:.0f}°F")
        self.query_one("#conditions", Label).update(c.condition)

        self.query_one("#detail-feels-like", Label).update(f"Feels like  {c.feels_like:.0f}°F")
        self.query_one("#detail-humidity", Label).update(f"Humidity    {c.humidity}%")
        self.query_one("#detail-wind", Label).update(f"Wind        {c.wind_speed:.0f} mph")
        self.query_one("#detail-uv", Label).update(f"UV Index    {c.uv_index:.1f}")
        self.query_one("#detail-precip", Label).update(f"Precip.     {c.precipitation:.1f} mm")

        forecast_lines = []
        for day in data.daily:
            abbr = DAY_ABBR[day.date.weekday()]
            forecast_lines.append(
                f"{abbr}  {day.temp_min:.0f}°–{day.temp_max:.0f}°  {day.condition}"
            )
        self.query_one("#forecast-text", Label).update("\n".join(forecast_lines))

        sparkline = self.query_one("#temp-sparkline", Sparkline)
        sparkline.data = data.hourly_temps

    def display_error(self, error: str) -> None:
        self.query_one("#loading", LoadingIndicator).display = False
        self.query_one("#temperature", Label).update("Error")
        self.query_one("#conditions", Label).update(error)
