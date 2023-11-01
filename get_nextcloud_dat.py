import caldav
from caldav.elements import dav, cdav
import datetime
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

if calendar is not None:
    todos = calendar.todos()

    for todo in todos:
        icalendar = Calendar.from_ical(todo.data)
        for component in icalendar.walk():
            if component.name == "VTODO":
                print(f"Task: {component.get('summary')}, Status: {component.get('status')}")
else:
    print(f"Calendar '{calendar_name}' not found")