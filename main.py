from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import randint

import csv


def date_range(start, stop, step):
    while start < stop:
        yield start.date()
        start += step


def time_track(entry, extras=None):
    deltas = [
        relativedelta(hours=0),  # Entry time
        relativedelta(hours=4),  # Out for lunch
        relativedelta(hours=5),  # Back from lunch
        relativedelta(hours=9)  # Going home
    ]

    if extras is not None:
        try:
            for i, extra in enumerate(extras):
                deltas[i] += extra
        except IndexError:
            pass

    return tuple(entry + d for d in deltas)


def extra_minutes(entry=None, lunch=None, exit=None):
    min_entry = 0 if entry is None else randint(*entry)
    min_lunch = (0 if lunch is None else randint(*lunch)) + min_entry
    min_exit = (0 if exit is None else randint(*exit)) + min_entry

    minutes = []
    for minute in [min_entry, min_lunch, min_lunch, min_exit]:
        minutes.append(relativedelta(minutes=minute))

    return minutes


def generate(begin, intervals):
    end = begin + relativedelta(months=1)
    step = relativedelta(days=1)

    for day in date_range(begin, end, step):
        if day.weekday() in [5, 6]:
            yield (day, None, None, None, None)
            continue

        add_time = extra_minutes(*intervals)
        day_tracking = [track.time() for track in time_track(begin, add_time)]

        yield (day, *day_tracking)


if __name__ == '__main__':
    start_date = datetime(2019, 8, 16, 13, 0)
    intervals = [(0, 10)]
    header = ('Date', 'Entry', 'Out for Lunch', 'Back from Lunch', 'Exit')

    with open('output.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)

        f_csv.writerows(generate(start_date, intervals))
