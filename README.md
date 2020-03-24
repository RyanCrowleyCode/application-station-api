# Application Station Django REST API

This API provides a way to interface with the database for Application Station. The corresponding repository for the React application can be found here:
https://github.com/RyanCrowleyCode/application-station


## Steps to get the Application Station API started

1. Create a new directory in your terminal. Clone down this repository by clicking the "Clone or Download" button above, copying the SSH key, and running the following command in your terminal `git clone sshKeyGoesHere`.
2. `cd applicationstationapi`
3. Create your OSX virtual environment in Terminal:

  - `python -m venv appstationenv`
  - `source ./appstationenv/bin/activate`

- Or create your Windows virtual environment in Command Line:

  - `python -m venv appstationenv`
  - `source ./appstationenv/Scripts/activate`

4. Install the app's dependencies:

  - `pip install -r requirements.txt`

5. Build your database from the existing models:

  - `python manage.py makemigrations appstationapp`
  - `python manage.py migrate`

6. Create a superuser for your local version of the app:

  - `python manage.py createsuperuser`

7. Populate your database with initial data from fixtures files: (_NOTE: every time you run this it will remove existing data and repopulate the tables_)

  - `python manage.py loaddata */fixtures/*.json`

8. Fire up your dev server and get to work!

  - `python manage.py runserver`




## Front-End Client

- This API is dependent on the front-end client. You can find it here:
https://github.com/RyanCrowleyCode/application-station


# Fetch calls

Should you choose leverage this API for your own front-end application, please reference the example fetch calls to the endpoints below to see some of the capability of this API. Please note that you will need to pass the Token in the headers for most requests.

Please note that the use of `${}` is to indicate string interpolation. Replace everything inside of `${}` with the value indicated inside of the brackets.
For example, to get the company with the ID of 1, replace `http://localhost:8000/companies/${id}` with `http://localhost:8000/companies/1`


## Users

- Fetch call to register a new user (POST)
  - `http://localhost:8000/register`
  - `{"email": "", "password": "", "first_name": "", "last_name": ""}`

- Fetch call to login an existing user (POST)
  - `http://localhost:8000/login`
  - `{"username": "", "password": ""}`


## Companies

- Fetch call to GET one company by company id:
  - `http://localhost:8000/companies/${id}`

- Fetch call to GET all companies:
  - `http://localhost:8000/companies`

- Fetch call to GET company based on name:
  - `http://localhost:8000/companies?name=${name}`

- Fetch call to POST company:
  - `http://localhost:8000/companies`
  - `{"name": ""}`


## Events

Events are user specific. You must pass a valid token in the header:

- `Authorization: Token ${token}`


- Fetch call to POST event:
  - `http://localhost:8000/events`
  - `{"details": "", "start_time": "", "end_time": "", "job_id": ${id}}`

- Fetch call to GET one event by event id:
  - `http://localhost:8000/events/${id}`

- Fetch call to GET all events:
  - `http://localhost:8000/events`

- Fetch call to GET events based on job_id:
  - `http://localhost:8000/events?job_id=${job_id}`

- Fetch call to PUT one event by event id:
  - `http://localhost:8000/events/${id}`
  - `{"details": "", "start_time": "", "end_time": "", "job_id": ${id}}`

- Fetch call to DELETE one event by event id:
  - `http://localhost:8000/events/${id}`


## Jobs

Jobs are user specific. You must pass a valid token in the header:

- `Authorization: Token ${token}`


- Fetch call to POST job:
  - `http://localhost:8000/jobs`
  - `{"title": "", "description": "", "link": "", "status_id": ${id}, "company_id": ${id}}`

- Fetch call to GET one job by job id:
  - `http://localhost:8000/jobs/${id}`

- Fetch call to GET all jobs:
  - `http://localhost:8000/jobs`

- Fetch call to PUT one job by job id:
  - `http://localhost:8000/jobs/${id}`
  - `{"title": "", "description": "", "link": "", "status_id": ${id}, "company_id": ${id}}`

- Fetch call to DELETE one job by job id:
  - `http://localhost:8000/jobs/${id}`


## Questions

Questions are user specific. You must pass a valid token in the header:

- `Authorization: Token ${token}`


- Fetch call to POST question:
  - `http://localhost:8000/questions`
  - `{"question": "", "is_from_interviewer": ${boolean}}`

- Fetch call to GET one question by question id:
  - `http://localhost:8000/questions/${id}`

- Fetch call to GET all questions:
  - `http://localhost:8000/questions`

- Fetch call to PUT one question by question id:
  - `http://localhost:8000/questions/${id}`
  - `{"question": "", "is_from_interviewer": ${boolean}}`

- Fetch call to PUT answer to a question by question id:
  - `http://localhost:8000/questions/${id}?answer=true`
  - `{"question": "", "is_from_interviewer": ${boolean}, "answer": ""}`

- Fetch call to DELETE one question by question id:
  - `http://localhost:8000/questions/${id}`


## Statuses

- Fetch call to GET all statuses:
  - `http://localhost:8000/statuses`

- Fetch call to get one status by status id:
  - `http://localhost:8000/statuses/${id}`