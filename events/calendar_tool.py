from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Event_Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Event_Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = Event.objects.filter(start__day=day)
        d = ''
        for event in events_per_day:
            d += f'<a href=/events/edit><li> {event.title} </li></a>'

        if day != 0:
            return f"<td><span class='date'><a href=/evetns/new_event >{day}</span></a><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events_per_month = Event.objects.filter(start__year=self.year, start__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events_per_month)}\n'
        return cal