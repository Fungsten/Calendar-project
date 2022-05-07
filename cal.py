from conf.config import CONFIG
from utils.sql_builder import SQLBuilder


class Cal():

    def __init__(self) -> None:
        pass

if __name__=="__main__":
    builder = SQLBuilder()
    c = builder.create_server_connection()
    builder.hard_reset(c, "calendar")

    # Eventually build out tables here
    builder.create_database(c, "calendar")
    b = builder.create_db_connection("calendar")

    create_events_table = '''
    CREATE TABLE event (
        event_id INT PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        location VARCHAR(40) NOT NULL,
        start_time DATETIME,
        end_time DATETIME,
        is_all_day BOOL NOT NULL
    );
    '''

    create_person_table = '''
    CREATE TABLE person (
        person_id INT PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        email VARCHAR(40) NOT NULL
    );
    '''

    builder.execute_query(b, create_events_table)
    builder.execute_query(b, create_person_table)

    create_participant_table = '''
    CREATE TABLE participate_event (
        person_id INT,
        event_id INT,
        PRIMARY KEY(person_id, event_id),
        FOREIGN KEY(person_id) REFERENCES person(person_id) ON DELETE CASCADE,
        FOREIGN KEY(event_id) REFERENCES event(event_id) ON DELETE CASCADE
    );
    '''

    builder.execute_query(b, create_participant_table)

    populate_people = '''
    INSERT INTO person VALUES
    (1, 'Mario', 'mmario@mushroom.kngd'),
    (2, 'Donkey Kong', 'dk@kong.isle'),
    (3, 'Link', 'hero@hyrule.cstl'),
    (4, 'Samus Aran', 'saran@metroid.met'),
    (5, 'Pikachu', 'pika@kanto.pok'),
    (6, 'Fox McCloud', 'starfox@corneria.pla'),
    (7, 'Kirby', 'kirby@dream.land'),
    (8, 'Yoshi', 'notyoshi@taxevasion.isle')
    '''

    builder.execute_query(b, populate_people)
