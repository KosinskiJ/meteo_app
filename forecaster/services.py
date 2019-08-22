import datetime


def generate_next_five_dates(forecast_type=None):
    counter = None
    if forecast_type == '24':
        counter = 1
    elif forecast_type == '48':
        counter = 2

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    dates = []
    for i in range(0, 5 * counter, counter):
        dates.append([(tomorrow + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
                      (tomorrow + datetime.timedelta(days=i + counter)).strftime("%Y-%m-%d")])

    return dates

