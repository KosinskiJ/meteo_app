from darksky import forecast


def get_closest_datetime(begin_date, latitude, longitude):
    API_KEY = "3ca98f3fbb052f57b5f9b89ecd28a162"
    weather_forecast = forecast(API_KEY, latitude, longitude, lang='pl', units='si', extend='hourly')
    times = list()
    hourly_list = weather_forecast.hourly

    for i in hourly_list:
        times.append(i.time)

    closest_datetime = min(times, key=lambda x: abs(x - begin_date))

    return closest_datetime, weather_forecast


def get_12h_forecast_darksky(begin_date, latitude, longitude):
    closest_time, weather_forecast = get_closest_datetime(begin_date, latitude, longitude)

    index_of_beginning = 0
    for i, obj in enumerate(weather_forecast.hourly):
        if obj.time == closest_time:
            index_of_beginning = i
            break

    clipped_to_12h = weather_forecast.hourly[index_of_beginning:index_of_beginning + 12]
    return clipped_to_12h


def generalize(list):
    generalized_value = sum(list) / len(list)
    return generalized_value


def get_generalized_darksky_forecast(begin_date, latitude, longitude):
    clipped_12 = get_12h_forecast_darksky(begin_date, latitude, longitude)

    cloudCover = list()
    dewPoint = list()
    humidity = list()
    icon = list()
    ozone = list()
    precipIntensity = list()
    precipProbability = list()
    precipType = list()
    pressure = list()
    summary = list()
    temperature = list()
    uvIndex = list()
    visibility = list()
    windBearing = list()
    windGust = list()
    windSpeed = list()

    for obj in clipped_12:
        cloudCover.append(obj.cloudCover)
        dewPoint.append(obj.dewPoint)
        humidity.append(obj.humidity)
        icon.append(obj.icon)
        ozone.append(obj.ozone)
        pressure.append(obj.pressure)
        temperature.append(obj.temperature)
        uvIndex.append(obj.uvIndex)
        visibility.append(obj.visibility)
        windBearing.append(obj.windBearing)
        windGust.append(obj.windGust)
        windSpeed.append(obj.windSpeed)
        summary = obj.summary

        if obj.precipProbability == 0:
            continue
        precipIntensity.append(obj.precipIntensity)
        precipProbability.append(obj.precipProbability)
        precipType = obj.precipType

    generalized_12h = {
        'cloud_cover': round(generalize(cloudCover), 2),
        'dev_point': round(generalize(dewPoint), 2),
        'humidity': round(generalize(humidity), 2),
        'ozone': round(generalize(ozone), 2),
        'pressure': round(generalize(pressure), 2),
        'temperature': round(generalize(temperature), 2),
        'uv_index': round(generalize(uvIndex), 2),
        'visibility': round(generalize(visibility), 2),
        'wind_bearing': round(generalize(windBearing), 2) if windBearing == 0 else 0,
        'wind_gust': round(generalize(windGust), 2) if windGust == 0 else 0,
        'wind_speed': round(generalize(windSpeed), 2) if windSpeed == 0 else 0,
        'precip_intensity': round(generalize(precipIntensity), 2) if precipIntensity == 0 else 0,
        'precip_probability': round(generalize(precipProbability), 2) if precipProbability == 0 else 0,
        'precip_type': precipType if precipProbability == "" else "",
        'summary': summary,
    }

    return generalized_12h

# GENERALIZED_MOCK = {
#     "cloud_cover": 0.98,
#     "dev_point": 1.54,
#     "humidity": 0.96,
#     "ozone": 332.34,
#     "precip_intensity": 0.09,
#     "precip_probability": 0.23,
#     "precip_type": "rain",
#     "pressure": 1006.28,
#     "summary": "Duże zachmurzenie",
#     "temperature": 1.97,
#     "uv_index": 0.08,
#     "visibility": 13.82,
#     "wind_bearing": 244.16,
#     "wind_gust": 12.19,
#     "wind_speed": 4.48,
# }
