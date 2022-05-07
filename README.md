# Calendar-project

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
