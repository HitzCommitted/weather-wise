import datetime
import requests
from dotenv import dotenv_values
from django.shortcuts import render


# Create your views here.
config = dotenv_values(".env")


def index(request):
    WEATHER_API_KEY = config["WEATHER_API_KEY"]
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    )
    # forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        # weather_data1, daily_forecast1 = fetch_weather_and_forecast(
        #     city1, WEATHER_API_KEY, current_weather_url, forecast_url
        # )
        weather_data1 = fetch_weather_and_forecast(
            city1, WEATHER_API_KEY, current_weather_url
        )

        if city2:
            # weather_data2, daily_forecast2 = fetch_weather_and_forecast(
            #     city2, WEATHER_API_KEY, current_weather_url, forecast_url
            # )
            weather_data2 = fetch_weather_and_forecast(
                city2, WEATHER_API_KEY, current_weather_url
            )
        else:
            # weather_data2, daily_forecast2 = None, None
            weather_data2 = None, None

        context = {
            "weather_data1": weather_data1,
            # "daily_forecast1": daily_forecast1,
            "weather_data2": weather_data2,
            # "daily_forecast2": daily_forecast2,
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    # forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    # daily_forecasts = []
    # for daily_data in forecast_response["daily"][:5]:
    #     daily_forecasts.append(
    #         {
    #             "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
    #             "min_temp": round(daily_data["temp"]["min"] - 273.15, 2),
    #             "max_temp": round(daily_data["temp"]["max"] - 273.15, 2),
    #             "description": daily_data["weather"][0]["description"],
    #             "icon": daily_data["weather"][0]["icon"],
    #         }
    #     )

    # return weather_data, daily_forecasts
    return weather_data
