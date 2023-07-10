# Import your dependencies
from dotenv import load_dotenv
import os
from nylas import APIClient  # type: ignore
from nicegui import ui
from datetime import date
from datetime import datetime
from dataclasses import dataclass
from typing import List

# Load your env variables
load_dotenv()

# Initialize an instance of the Nylas SDK using the client credentials
nylas = APIClient(
    os.environ.get("CLIENT_ID"),
    os.environ.get("CLIENT_SECRET"),
    os.environ.get("ACCESS_TOKEN"),
)

@dataclass # Class decorator
class EventItems:
    event_name: str

# To hold events
events: List[EventItems] = [

]

@dataclass # Class decorator
class EmailItems:
    email_name: str

# To hold emails
emails: List[EmailItems] = [

]

# Get list of events
def get_events(current_date) -> None:
    # Get today's date as Year, month, day
    today_date = datetime.strptime(current_date, '%Y-%m-%d').date() 
    # Today’s date at 12:00:00 am
    AFTER = int(datetime(today_date.year, today_date.month, today_date.day, 0, 0, 0).strftime('%s'))
    # Today’s date at 11:59:59 pm 
    BEFORE = int(datetime(today_date.year, today_date.month,today_date.day, 23, 59, 59).strftime('%s'))
    # Get all events in the specified range
    events = nylas.events.where(calendar_id=os.environ.get("CALENDAR_ID"),  starts_after = AFTER, ends_before = BEFORE)
    # Auxiliary variables
    event_info = ""
    counter = 0
    # Loop events
    for event in events:
        counter += 1
        # Does the event have a start and end time?
        if "start_time" in event.when:
			# Grab from and end time, as well as the event title
            event_info = f"From:  {datetime.fromtimestamp(event.when['start_time']).strftime('%H:%M:%S')} \
                                 To: {datetime.fromtimestamp(event.when['end_time']).strftime('%H:%M:%S')} \
                                 | {event.title}"
            add(event_info, "event")
        # Does the event last all day?    
        else:
			# As an all day event, simply grab the title 
            add(f"All day event | {event.title}")
    # No events?
    if counter == 0:
        add("No events today", "event")		

# Get list of emails
def get_emails(current_date) -> None:
    # Get today's date as Year, month, day
    today_date = datetime.strptime(current_date, '%Y-%m-%d').date() 
    # Today’s date at 12:00:00 am
    AFTER = int(datetime(today_date.year, today_date.month, today_date.day, 0, 0, 0).strftime('%s'))
    # Today’s date at 11:59:59 pm 
    BEFORE = int(datetime(today_date.year, today_date.month,today_date.day, 23, 59, 59).strftime('%s'))	
    # Get all emails in the specified range
    messages = nylas.messages.where(in_ = "inbox", unread = "true", limit = 5, received_after = AFTER, received_before = BEFORE)
    # Auxiliary variables
    email_info = ""
    counter = 0
    # Loop emails    
    for message in messages:
        counter += 1
        # Grab the time, who's sending the email and the title of the email
        email_info = f"Time: {datetime.fromtimestamp(message.date).strftime('%H:%M:%S')} \
                             | From: {message.from_[0]['name']} | Title: {message.subject}"
        add(email_info, "email")
    # No emails?
    if counter == 0:
        add("No new emails today", "email")

# Function to add events and emails		
def add(name: str, type_ : str) -> None:
    # If it's an event, add it to the events list
    if type_ == "event":
        events.append(EventItems(name))
        render_events_list.refresh()
    # If it's an email, add it to the email list
    else:
        emails.append(EmailItems(name))
        render_emails_list.refresh()         

# Clear the list of events
def clear_events() -> None:
    events.clear()

# Clear the list of emails
def clear_emails() -> None:
    emails.clear()

# When we click on the calendar 
# to select a new date
def handle_input(e):
    # We pass the selected date
    current_date = e.value
    # If for some reason, there's no date
    # grab the current date
    if current_date is None:
        date.today()
        current_date = str(date.today())
    clear_events()
    # Get events for the selected date
    get_events(current_date)
    clear_emails()
    # Get emails for the selected date
    get_emails(current_date)

# Decorator to refresh the events list
@ui.refreshable
def render_events_list():
    # Title using Tailwind CSS
    ui.label('Events').tailwind.font_weight('black').font_size('4xl').text_color('blue-700')
    # Loop events
    for event in events:
        # Put events one after the other
        with ui.row().classes('items-center'):
            # Detail of event
            ui.label(event.event_name).tailwind.font_weight('semibold').font_size('lg')

# Decorator to refresh the emails list            
@ui.refreshable
def render_emails_list():
    # Title using Tailwind CSS
    ui.label('Emails').tailwind.font_weight('black').font_size('4xl').text_color('blue-700')
    # Loop emails
    for email in emails:
       # Put events one after the other
        with ui.row().classes('items-center'):
            # Detail of event
            ui.label(email.email_name).tailwind.font_weight('semibold').font_size('lg')

# Main layout with everything centered
with ui.column().classes('w-full items-center'):
    # Get today's date
    today = date.today()
    current_date = str(date.today())
    # Clear all events and emails	
    clear_events()
    clear_emails()
    # Set application title
    ui.label('Daily Planner').tailwind.font_weight('black').font_size('6xl').text_color('blue-700')
    # Create the calendar widget
    ui.date(value=today, on_change=handle_input)
    # Show all events
    get_events(current_date)
    render_events_list()
    # Show all emails
    get_emails(current_date)
    render_emails_list()

# Run our application
ui.run(title = 'NiceGUI Planner')
