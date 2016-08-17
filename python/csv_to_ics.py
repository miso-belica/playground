# -*- coding: utf-8 -*-

"""
Converts CSV file with birthdays into ICS (calendar) file.
CSV file is in format "name,birthday_date".

Setup:
    pip install docopt

Usage:
    convert --csv=<file> --ics=<file>
"""

import csv
import uuid
import datetime

from docopt import docopt


_CALENDAR_TEMPLATE = """
BEGIN:VCALENDAR
PRODID:-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN
VERSION:2.0
{events}
END:VCALENDAR
"""
_EVENT_TEMPLATE = """
BEGIN:VEVENT
CREATED:20160817T133426Z
LAST-MODIFIED:20160817T133555Z
DTSTAMP:20160817T133555Z
UID:{uuid}
SUMMARY:{title}
RRULE:FREQ=YEARLY
CATEGORIES:Birthday
DTSTART;VALUE=DATE:{date}
DTEND;VALUE=DATE:{date}
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
TRIGGER;VALUE=DURATION:-P2W
END:VALARM
END:VEVENT
"""


def create_birthday_event(name, date):
    event = _EVENT_TEMPLATE.format(
        uuid=uuid.uuid4().hex,
        title=name,
        date=date.strftime("%Y%m%d")
    )

    return event.strip()


def create_calendar(events):
    return _CALENDAR_TEMPLATE.format(events="\n".join(events)).strip()


def main(args):
    events = []
    with open(args["--csv"], "r", encoding="utf-8") as file:
        for name, date in csv.reader(file):
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            events.append(create_birthday_event(name, date))

    with open(args["--ics"], "w", encoding="utf-8") as file:
        file.write(create_calendar(events))


if __name__ == "__main__":
    main(docopt(__doc__))
