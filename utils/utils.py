import datetime

def _get_today():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def _shiftdays(date, days):
    datetime_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    shifted_date = datetime_date + datetime.timedelta(days=days)
    new_date = shifted_date.strftime("%Y-%m-%d")
    return new_date