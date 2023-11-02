import caldav
from caldav.elements import dav, cdav
from datetime import datetime
from icalendar import Calendar
from dotenv import load_dotenv
import os

# load the environment variables from .env
load_dotenv()

# Set up the client
url = os.getenv('url')
username = os.getenv('username')
password = os.getenv('password')
client = caldav.DAVClient(url=url, username=username, password=password)

# Find the calendar
principal = client.principal()
calendars = principal.calendars()
#calendar = calendars[9]  # Use the first calendar

# Define the name of the calendar you want to access
calendar_name = "SmartScreen"
# Find the calendar by its name
calendar = next((cal for cal in calendars if cal.name == calendar_name), None)



def get_todos():
    todos_list = []
    if calendar is not None:
        todos = calendar.todos()
        for todo in todos:
            icalendar = Calendar.from_ical(todo.data)
            for component in icalendar.walk():
                if component.name == "VTODO":
                    start_date = component.get('dtstart')
                    due_date = component.get('due')
                    completed_date = component.get('completed')
                    # Convert to datetime and then to string
                    if start_date is not None:
                        start_date = start_date.dt.strftime('%Y-%m-%d %H:%M:%S')
                    if due_date is not None:
                        due_date = due_date.dt.strftime('%Y-%m-%d %H:%M:%S')
                    if completed_date is not None:
                        completed_date = completed_date.dt.strftime('%Y-%m-%d %H:%M:%S')
                    todos_list.append({
                        'summary': str(component.get('summary')),
                        'status': str(component.get('status')),
                        'description': str(component.get('description')),
                        'due': due_date,
                        'start_date': start_date,
                        'priority': str(component.get('priority')),
                        'completed_date': completed_date
                    })
    else:
        print(f"Calendar '{calendar_name}' not found")
    return todos_list

def fetch_calendar_entries(start_date_str='2023-11-01', end_date_str='2023-11-03'):
    # Convert string to datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    entries_list = []
    # Get ignored calendars from environment variable
    ignored_calendars = os.getenv('IGNORED_CALENDARS', '').split(',')

    for calendar in calendars:
        # Skip ignored calendars
        if calendar.name in ignored_calendars:
            continue

        # Fetch events within the specified time frame
        events = calendar.date_search(start_date, end_date)

        for event in events:
            icalendar = Calendar.from_ical(event.data)
            for component in icalendar.walk():
                if component.name == "VEVENT":
                    start_date_event = component.get('dtstart')
                    end_date_event = component.get('dtend')
                    summary = component.get('summary')
                    description = component.get('description')
                    # Convert to datetime and then to string
                    if start_date_event is not None:
                        start_date_event = start_date_event.dt.strftime('%Y-%m-%d %H:%M:%S')
                    if end_date_event is not None:
                        end_date_event = end_date_event.dt.strftime('%Y-%m-%d %H:%M:%S')
                    entries_list.append({
                        'calendar': calendar.name,
                        'summary': str(summary),
                        'description': str(description),
                        'start_date': start_date_event,
                        'end_date': end_date_event
                    })
    return entries_list

def print_calendar_names():
    calendars = principal.calendars()
    for calendar in calendars:
        print(calendar.name)

if __name__ == '__main__':
    results = fetch_calendar_entries()
    for todo in results:
        print(todo['summary'])
