from datetime import datetime
from distutils.command.build import build
from typing import Dict, List

from fastapi import FastAPI, Response

from app.event import Event
from app.person import Person
from conf.config import CONFIG
from utils.emailer import Emailer
from utils.sql_builder import SQLBuilder

app = FastAPI()

emailer = Emailer("init@smashbros.nin")
builder = SQLBuilder()
c = builder.create_db_connection(CONFIG.get('db_name'))

@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
○ Read event
○ Create event (with participants)
○ Update event (including participants)
○ Delete event
○ Get events (mine and any where I am a participant, filterable by time range)
'''

@app.get("/events")
async def get_all_events():
    '''
    Gets all events.
    ''' 
    return builder.read_all_from_table(c, 'event')

@app.get("/events/{event_id}")
async def get_event(event_id: int):
    '''
    Gets specific event by ID.
    '''
    return builder.read_from_table_by_id(c, 'event', event_id)

@app.get("/people")
async def get_all_people():
    '''
    Gets all people.
    '''
    return builder.read_all_from_table(c, 'person')

@app.get("/people/{person_id}")
async def get_person(person_id: int):
    '''
    Gets specific person by ID.
    '''
    return builder.read_from_table_by_id(c, 'person', person_id)

@app.get("/myevents/{person_id}")
async def get_my_events(person_id: int, start_time: str=None, end_time: str=None):
    '''
    Gets all events pertinent to a specific person by ID.
    Optional parameters for events that begin between the start_time and end_time.
    '''
    if start_time:
        begin = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S')
    if end_time:
        end = datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%S')

    events = []
    data = builder.read_from_table_by_id(c, 'participate_event', person_id, 'person')
    for entry in data:
        event_id = entry.get('event_id')
        event = builder.read_from_table_by_id(c, CONFIG.get('event_table'), event_id)

        if start_time and not end_time:
            if event[0].get('start_time') >= begin:
                events.append(event)
        elif not start_time and end_time:
            if event[0].get('start_time') <= end:
                events.append(event)
        elif start_time and end_time:
             if event[0].get('start_time') >= begin and event[0].get('start_time') <= end:
                 events.append(event)
    return events

@app.post("/people")
async def add_person(person: Person):
    '''
    Adds a person. Requires name and email information.
    '''
    builder.add_person(c, person.name, person.email)
    return person

@app.post("/events")
async def add_event(event: Event):
    '''
    Adds an event. Requires name, location, start_time, end_time, and is_all_day information.
    '''
    builder.add_event(c, event.name, event.location, event.start_time, event.end_time, event.is_all_day, event.participants)
    emails = []
    for person in event.participants:
        emails.append(builder.get_person_email(c, person))
    emailer.add_event(event.name, emails)
    return event

@app.delete("/people/{person_id}")
async def remove_person(person_id: int):
    '''
    Deletes a specific person by ID.
    '''
    builder.delete_item_by_id(c, person_id, CONFIG.get("person_table"))
    return { "deleted": True }

@app.delete("/events/{event_id}")
async def remove_event(event_id: int):
    '''
    Deletes a specific event by ID.
    '''
    event_name = builder.get_event_name(c, event_id)

    # gather participant emails
    emails = []
    event_to_participants = builder.read_from_table_by_id(c, CONFIG.get("participant_table"), event_id, 'event')
    for part in event_to_participants:
        person = part.get('person_id')
        emails.append(builder.get_person_email(c, person))

    builder.delete_item_by_id(c, event_id, CONFIG.get("event_table"))
    emailer.remove_event(event_name, emails)
    return { "deleted": True }

@app.patch("/events/{event_id}")
async def update_event(event_id: int, update: Dict[str, str], participants: List[int]):
    '''
    Updates a specific event by ID. Arg update should contain only the changes.
    Arg participants should be the updated list.
    '''
    event_name = builder.get_event_name(c, event_id)

    # gather participant emails
    prev_emails = []
    prev_participants = set()
    event_to_participants = builder.read_from_table_by_id(c, CONFIG.get("participant_table"), event_id, 'event')
    for part in event_to_participants:
        person = part.get('person_id')
        prev_participants.add(person)
        prev_emails.append(builder.get_person_email(c, person))

    builder.update_item_by_id(c, event_id, 'event', update)

    # gather participant emails
    new_emails = []
    new_participants = []
    for part in participants:
        person = part.get('person_id')
        if person in prev_participants:
            prev_participants.remove(person)
        else:
            new_emails.append(builder.get_person_email(c, person))
            new_participants.append(person)

    for p in prev_participants:
        builder.delete_participant(c, p, event_id)
    builder.add_participants(c, new_participants, event_id)

    emailer.update_event(event_name, event_id)
    return update
