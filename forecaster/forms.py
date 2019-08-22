from django.forms import ModelForm, HiddenInput

from dashboard.models import OneDayForecast, WeatherForecast, TwoDayForecast, SynopticSituation


class OneDayForecastForm(ModelForm):
    class Meta:
        model = OneDayForecast
        exclude = ('weather_forecast1', 'weather_forecast2')
        widgets = {
            'created_by': HiddenInput(),
            'modified_by': HiddenInput(),
            'forecast_type_order': HiddenInput(),
        }


class TwoDayForecastForm(ModelForm):
    class Meta:
        model = TwoDayForecast
        exclude = ('weather_forecast1', 'weather_forecast2', 'weather_forecast3', 'weather_forecast4',)
        widgets = {
            'created_by': HiddenInput(),
            'modified_by': HiddenInput(),
            'forecast_type_order': HiddenInput(),
        }


class WeatherForecastForm(ModelForm):
    class Meta:
        model = WeatherForecast
        exclude = ()