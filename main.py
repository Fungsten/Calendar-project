from fastapi import FastAPI, Response

from conf.config import CONFIG
from utils.sql_builder import SQLBuilder

from app.person import Person
from app.event import Event

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/events")
async def get_all_events():
    builder = SQLBuilder()
    c = builder.create_db_connection(CONFIG.get('db_name'))

    r = builder.read_all_from_table(c, 'event')
    data = builder.load_event_into_pd(r)
    return Response(content = builder.df_to_json(data))

@app.get("/events/{event_id}")
async def get_event(event_id: int):
    builder = SQLBuilder()
    c = builder.create_db_connection(CONFIG.get('db_name'))

    r = builder.read_from_table_by_id(c, 'event', event_id)
    data = builder.load_event_into_pd(r)
    return Response(content = builder.df_to_json(data))

@app.get("/people")
async def get_all_people():
    builder = SQLBuilder()
    c = builder.create_db_connection(CONFIG.get('db_name'))

    r = builder.read_all_from_table(c, 'person')
    data = builder.load_person_into_pd(r)
    return Response(content = builder.df_to_json(data))

@app.get("/people/{person_id}")
async def get_person(person_id: int):
    builder = SQLBuilder()
    c = builder.create_db_connection(CONFIG.get('db_name'))

    r = builder.read_from_table_by_id(c, 'person', person_id)
    data = builder.load_person_into_pd(r)
    return Response(content = builder.df_to_json(data))

@app.post("/people")
async def add_person(person: Person):
    print(person.name)
    return person

@app.post("/event")
async def add_event(event: Event):
    return event