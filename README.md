# Calendar-project

# Instructions

Backend
Create a REST API for managing a user’s calendar.

Notes:
● You don’t need to implement authentication, and can just hard-code a “current user” object somewhere that would normally be
populated by an auth system
● If you identify functionality you think might be appropriate for a production version of the application, but has not explicitly
been mentioned as required, feel free to implement it or just add comments with your thought process and potential next
steps

Requirements:

● Create a SQL database and implement the necessary DB schema for your application
● Create a REST API that can handle the following scenarios:
○ Read event
○ Create event (with participants)
○ Update event (including participants)
○ Delete event
○ Get events (mine and any where I am a participant, filterable by time range)
● Participants should be notified via email when they’re added to an event, or of any changes
○ You can just stub out an email-sending module that logs to the console instead of actually sending an email
● Include unit tests as you see fit

# Virtual Environment Setup

`python3 -m venv env`

`.\env\Scripts\activate`

`python3 -m pip install -r requirements.txt`

Start the server:
`uvicorn main:app`

Once the server is up:

- Interactive API docs: `http://127.0.0.1:8000/docs`
- Alternative: `http://127.0.0.1:8000/redoc`

# Units Tests

From the top level directory:
`python3 -m pytest`
