from datetime import datetime, timedelta

def format_day(day_str):
    date = datetime.strptime(day_str, '%Y-%m-%d')
    today = datetime.now()
    diff_days = (today - date).days
    is_same_month = diff_days < today.day
    if is_same_month:
        return date.strftime('%A %d')
    else:
        return date.strftime('%A %d/%m')

def extract_time(seconds_str):
    time = timedelta(seconds=int(seconds_str))
    hours, rem = divmod(time.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return hours, minutes, seconds

def format_time(seconds_str):
    if seconds_str is None:
        return "N/A"
    return "{0:02d}:{1:02d}:{1:02d}".format(*extract_time(seconds_str))

def format_duration(seconds_str):
    if seconds_str is None:
        return "N/A"
    return "{0:02d}:{1:02d}:{2:02d}".format(*extract_time(seconds_str))