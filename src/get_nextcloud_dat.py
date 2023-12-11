import caldav
from datetime import datetime, timedelta, date, time
from config import username, password, caldav_url, IGNORED_CALENDARS
from dateutil import tz
from icalendar import Calendar
import sys
import os
import requests

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(script_directory)


def get_calendars():
    client = caldav.DAVClient(url=caldav_url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    return calendars

def get_dates(start_date_str=None, end_date_str=None, now=None):
    # Define local timezone
    local_tz = tz.tzlocal()

    if start_date_str is None:
        start_date_str = now.strftime('%Y-%m-%d')
    if end_date_str is None:
        end_date_str = (now + timedelta(days=2)).strftime('%Y-%m-%d')
    
    # Convert string to datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    return start_date, end_date, local_tz

def filter_events(events, now, current_date, current_hour, calendar, local_tz):
    entries_list = []

    for event in events:
        icalendar = Calendar.from_ical(event.data)
        for component in icalendar.walk():
            if component.name == "VEVENT":
                start_date_event = component.get('dtstart').dt
                end_date_event = component.get('dtend').dt
                print(component.get('summary')+str(type(start_date_event)))
                # Convert date to datetime if necessary
                if isinstance(start_date_event, date) and not isinstance(start_date_event, datetime):
                    #print(component.get('summary')+str(start_date_event))
                    start_date_event = datetime.combine(start_date_event, time.min, tzinfo=tz.tzlocal())
                if isinstance(end_date_event, date) and not isinstance(end_date_event, datetime):
                    #print(component.get('summary')+str(end_date_event))
                    end_date_event = datetime.combine(end_date_event, time.min, tzinfo=tz.tzlocal())

                # Filter out events based on the provided logic
                if end_date_event < now:
                    print("now: "+ str(now)+" end_date_event: "+str(end_date_event))
                    print("1"+component.get('summary'))
                    continue
                if current_hour < 18 and start_date_event.date() != current_date:
                   #print("2"+component.get('summary'))
                   continue
                if current_hour >= 18 and start_date_event.date() > current_date + timedelta(days=1):
                    #print("3"+component.get('summary'))
                    continue
 
                summary = component.get('summary')
                description = component.get('description')

                # Convert to local time zone
                if start_date_event is not None:
                    start_date_event = start_date_event.replace(tzinfo=tz.tzlocal()).astimezone(local_tz)
                    start_date_event = start_date_event.strftime('%Y-%m-%d %H:%M:%S')
                if end_date_event is not None:
                    end_date_event = end_date_event.replace(tzinfo=tz.tzlocal()).astimezone(local_tz)
                    end_date_event = end_date_event.strftime('%Y-%m-%d %H:%M:%S')
                
                entries_list.append({
                    'calendar': calendar.name,
                    'summary': str(summary),
                    'description': str(description),
                    'due': start_date_event,
                    'end_date': end_date_event
                })

    return entries_list

def fetch_calendar_entries(start_date_str=None, end_date_str=None, now=None):
    start_date, end_date, local_tz = get_dates(start_date_str, end_date_str, now)

    calendars = get_calendars()
    entries_list = []
    ignored_calendars = IGNORED_CALENDARS.split(',')

    # Get current date and hour
    now = datetime.now(tz=local_tz)
    current_date = now.date()
    current_hour = now.time().hour

    for calendar in calendars:
        # if calendar.name in ignored_calendars: # in case some calendars should be ignored
        #     continue

        events = calendar.date_search(start_date, end_date)
        entries_list += filter_events(events, now, current_date, current_hour, calendar, local_tz)

    entries_list = sorted(entries_list, key=lambda x: x['due'])
    return entries_list

def fetch_public_events(ical_urls=[], now=None):
    entries_list = []

    # Define local timezone
    local_tz = tz.tzlocal()

    # Get current date and hour
    current_date = now.date()
    current_hour = now.time().hour

    # Fetch and parse public iCal calendars
    for ical_url in ical_urls:
        response = requests.get(ical_url)
        icalendar = Calendar.from_ical(response.text)
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
                    start_date_event = start_date_event.replace(tzinfo=tz.tzlocal()).astimezone(local_tz)
                    start_date_event = start_date_event.strftime('%Y-%m-%d %H:%M:%S')
                if end_date_event is not None:
                    end_date_event = end_date_event.replace(tzinfo=tz.tzlocal()).astimezone(local_tz)
                    end_date_event = end_date_event.strftime('%Y-%m-%d %H:%M:%S')

                entries_list.append({
                    'calendar': 'Public Calendar',
                    'summary': str(summary),
                    'description': str(description),
                    'due': start_date_event,
                    'end_date': end_date_event
                })

    entries_list = sorted(entries_list, key=lambda x: x['due'])
    return entries_list

def fetch_all_events(start_date_str=None, end_date_str=None, now=None, ical_urls=[]):
    # Fetch events from Nextcloud calendars
    nextcloud_events = fetch_calendar_entries(start_date_str, end_date_str, now)

    # Fetch events from public iCal calendars
    public_events = fetch_public_events(ical_urls, now)

    # Combine and sort all events
    all_events = nextcloud_events + public_events
    all_events = sorted(all_events, key=lambda x: x['due'])

    return all_events

def print_calendar_names(principal):
    calendars = principal.calendars()
    for calendar in calendars:
        print(calendar.name)

if __name__ == '__main__':
    local_tz = tz.tzlocal()
    # get data:
    now = datetime.now(tz=local_tz)

    results = fetch_all_events(now=now, ical_urls=["https://obs.fbi.h-da.de/obs/service.php?action=getPersPlanAbo&lfkey=31dcbbef4835595bbd8d5b80dec45b9677c4ac2bba5516fb92ac5834c67de5d9e1adb098a86f0e36"])
    for todo in results:
        print(todo['summary'])
        print(todo['due'])
