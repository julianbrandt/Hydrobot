import datetime

timezones = {
    "UTC": 0,
    "GMT": 0,
    "PST": 16,
    "EST": 19,
    "AET": 10,
    "GST": 4,
    "AWST": 8,
    "WST": 13,
    "ADT": 21,
    "IST": 1,
    "CDT": 19,
    "CEST": 2,
    "CET": 1,
    "EDT": 20,
    "PDT": 17,
    "MDT": 18,
    "AST": 3
}


def timezone_current(timezone, commandtype=None):
    if commandtype is not None:
        return timezone_calculate(timezone, commandtype)
    if timezone not in timezones:
        return "The timezone `" + timezone + "` is not indexed by Hydrobot"

    now = datetime.datetime.utcnow()
    minute = now.minute
    hour = now.hour

    new_time = hour + timezones[timezone]
    if new_time > 23:
        new_time -= 24

    if len(str(new_time)) == 1:
        new_time = "0" + str(new_time)
    if len(str(minute)) == 1:
        minute = "0" + str(minute)

    return "It is currently `" + str(str(new_time) + ":" + str(minute)) + "` in " + timezone


def timezone_calculate(timezone, future_time):
    if timezone not in timezones:
        return "The timezone `" + timezone + "` is not indexed by Hydrobot"

    now = datetime.datetime.utcnow()
    minute = now.minute
    hour = now.hour

    new_hour = hour + timezones[timezone]
    if new_hour > 23:
        new_hour -= 24

    try:
        future_hour = int(future_time[0:2]) - new_hour - 1
        future_minute = int(future_time[3:5]) - minute
        if future_hour < 0:
            future_hour += 24
        if future_minute < 0:
            future_minute += 60
        if future_hour == 23 and int(future_time[3:5]) > minute:
            future_hour -= 23

    except:
        return None

    if len(str(future_hour)) == 1:
        future_hour = "0" + str(future_hour)
    if len(str(future_minute)) == 1:
        future_minute = "0" + str(future_minute)

    return "It will be `" + future_time + "` in " + timezone + " in `" + str(future_hour) + "` hours and `" + str(
        future_minute) + "` minutes"
