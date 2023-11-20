import caldav
from datetime import datetime, timedelta
from icalendar import Calendar
from config import username, password, caldav_url, IGNORED_CALENDARS
from dateutil import tz
import sys
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(script_directory)

def get_calendars():
    client = caldav.DAVClient(url=caldav_url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    return calendars

def fetch_calendar_entries(start_date_str=None, end_date_str=None, now=None):
    # Define local timezone
    local_tz = tz.tzlocal()

    if start_date_str is None:
        start_date_str = now.strftime('%Y-%m-%d')
    if end_date_str is None:
        end_date_str = (now + timedelta(days=2)).strftime('%Y-%m-%d')
    
    calendars = get_calendars()
    
    # Convert string to datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    entries_list = []
    ignored_calendars = IGNORED_CALENDARS.split(',')

    # Get current date and hour
    now = datetime.now(tz=local_tz)
    current_date = now.date()
    current_hour = now.time().hour

    for calendar in calendars:
        if calendar.name in ignored_calendars:
            continue

        events = calendar.date_search(start_date, end_date)

        for event in events:
            icalendar = Calendar.from_ical(event.data)
            for component in icalendar.walk():
                if component.name == "VEVENT":
                    start_date_event = component.get('dtstart').dt
                    end_date_event = component.get('dtend').dt

                    # Filter out events based on the provided logic
                    if end_date_event < now:
                        continue
                    if current_hour < 18 and start_date_event.date() != current_date:
                        continue
                    if current_hour >= 18 and start_date_event.date() > current_date + timedelta(days=1):
                        continue

                    summary = component.get('summary')
                    description = component.get('description')

                    # Convert to local time zone
                    if start_date_event is not None:
                        start_date_event = start_date_event.replace(tzinfo=tz.tzutc()).astimezone(local_tz)
                        start_date_event = start_date_event.strftime('%Y-%m-%d %H:%M:%S')
                    if end_date_event is not None:
                        end_date_event = end_date_event.replace(tzinfo=tz.tzutc()).astimezone(local_tz)
                        end_date_event = end_date_event.strftime('%Y-%m-%d %H:%M:%S')
                    
                    entries_list.append({
                        'calendar': calendar.name,
                        'summary': str(summary),
                        'description': str(description),
                        'due': start_date_event,
                        'end_date': end_date_event
                    })
    entries_list = sorted(entries_list, key=lambda x: x['due'])
    return entries_list

def print_calendar_names(principal):
    calendars = principal.calendars()
    for calendar in calendars:
        print(calendar.name)

# if __name__ == '__main__':
#     results = fetch_calendar_entries()
#     for todo in results:
#         print(todo['summary'])
