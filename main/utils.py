from datetime import datetime, timedelta

from django.conf import settings


def get_protocol():
    if settings.DEBUG:
        return "http:"
    else:
        return "https:"


def get_ics(event):
    begin_timestamp = datetime.strftime(event.scheduled_at, "%Y%m%dT%H%M%S")
    finish_date = event.scheduled_at + timedelta(hours=2)
    finish_timestamp = datetime.strftime(finish_date, "%Y%m%dT%H%M%S")

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:scihublondon/ics
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/London
BEGIN:DAYLIGHT
TZOFFSETFROM:+0000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
DTSTART:19810329T010000
TZNAME:GMT+1
TZOFFSETTO:+0100
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0100
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
DTSTART:19961027T020000
TZNAME:GMT
TZOFFSETTO:+0000
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
TRANSP:OPAQUE
DTEND;TZID=Europe/London:{finish_timestamp}
UID:{begin_timestamp}@scihublondon.org
DTSTAMP:{begin_timestamp}Z
LOCATION:Newspeak House\\, 133-135 Bethnal Green Road\\, E2 7DG
DESCRIPTION:https://scihublondon.org/{event.slug}/
URL;VALUE=URI:{event.location_url}
SEQUENCE:0
SUMMARY:Sci-Hub London {event.title}
LAST-MODIFIED:{begin_timestamp}Z
CREATED:{begin_timestamp}Z
DTSTART;TZID=Europe/London:{begin_timestamp}
END:VEVENT
END:VCALENDAR
"""
