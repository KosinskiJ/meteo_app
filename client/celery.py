from datetime import timedelta

from celery.task import periodic_task

from dashboard.models import ForecastType
from meteoapp.celery import app


@app.task(name="celery_test")
def change_weather_forecast_statuses():
    all_forecasts = ForecastType.objects.all()

    for forecast in all_forecasts:
        print(forecast)
