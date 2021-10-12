
# A very simple Bottle Hello World app for you to get started with...
import json, os
from datetime import datetime
from bottle import default_app, route, run, template, static_file, request
from formatters import *

JSON_BASE = '.'

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static') # might need to change to /static on production

@route('/partials/<filename>')
def server_static(filename):
    return static_file(filename, root='views/partials') # might need to change to /static on production

def pretty_timestamp(timestamp):
    return 0

@route('/')
def index():
    with open(os.path.join(JSON_BASE, 'andrew.json')) as fp:
        data = json.load(fp)
    days = data['days']
    days_sorted = []
    for day_str in sorted(days):
        day_data = days[day_str]
        entries = []
        previous_entry_time = None
        entry_duration = None
        for entry_time in sorted(day_data):
            entry_data = day_data[entry_time]
            if previous_entry_time is not None:
                entry_duration = int(entry_time) - int(previous_entry_time)
            previous_entry_time = entry_time
            entries.append({
                'time': format_time(entry_time),
                'duration': format_duration(entry_duration),
                'items': entry_data['items'],
                'comments': entry_data['comments'],
            })
        days_sorted.append({
            'day': format_day(day_str),
            'entries': entries
        })

    return template('index', days=days_sorted)

def get_day_and_time(timestring):
    timestamp = datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S')
    day_str = timestamp.strftime('%Y-%m-%d')
    time = timestamp.time()
    seconds = (time.hour * 60 * 60) + (time.minute * 60) + time.second
    #now = datetime.datetime.now()
    #midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    #seconds = (now - midnight).seconds
    return day_str, seconds


@route('/user')
def show_user():
    with open(os.path.join(JSON_BASE, 'andrew.json')) as fp:
        data = json.load(fp)
    '''
    log_entries = data['log_entries']
    sorted_log_entries = []
    previous_timestamp = None
    duration = None
    for timestring in sorted(log_entries):
        timestamp = datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S')
        if previous_timestamp is not None:
            duration = timestamp - previous_timestamp
        previous_timestamp = timestamp

        log_data = log_entries[timestring]
        sorted_log_entries.append({
            'timestamp': timestamp,
            'duration': duration,
            'items': log_data['items'],
            'comments': log_data['comments'],
        })
    '''
    days = data['days']
    days_sorted = []
    for day_str in sorted(days):
        day_data = days[day_str]
        entries = []
        previous_entry_time = None
        entry_duration = None
        for entry_time in sorted(day_data):
            entry_data = day_data[entry_time]
            if previous_entry_time is not None:
                entry_duration = int(entry_time) - int(previous_entry_time)
            previous_entry_time = entry_time
            entries.append({
                'time': format_time(entry_time),
                'duration': format_duration(entry_duration),
                'items': entry_data['items'],
                'comments': entry_data['comments'],
            })
        days_sorted.append({
            'day': format_day(day_str),
            'entries': entries
        })

    return template('index', days=days_sorted)


@route('/add_log', method='POST')
def add_log():
    data = request.json
    with open(os.path.join(JSON_BASE, 'andrew.json')) as fp:
        existing_data = json.load(fp)
    if not 'days' in existing_data:
        log_entries = existing_data['log_entries']
        log_entries[data['timestamp']] = data['log_data']
        days = {}
        for timestring in sorted(log_entries):

            log_data = log_entries[timestring]
            day_str, seconds = get_day_and_time(timestring)
            if day_str in days:
                day = days[day_str]
            else:
                day = {}
                days[day_str] = day
            day[seconds] = log_data
        existing_data['days'] = days
        del existing_data['log_entries']
    else:
        days = existing_data['days']
        day_str, seconds = get_day_and_time(data['timestamp'])
        # Create day if doesn't exist
        if day_str in days:
            day = days[day_str]
        else:
            day = {}
            days[day_str] = day
        day[seconds] = data['log_data']

    with open(os.path.join(JSON_BASE, 'andrew.json'), 'w') as fp:
        json.dump(existing_data, fp, indent=4)
    return {'response': 'OK'}


application = default_app()
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)
