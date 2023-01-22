# General info

<strong>THE APP in first stage of development. Backend/ frontend services under construction.</strong>

Django/ Vue web app for gathering real estate announces from various web sites in order to present result to the user accordingly to his criteria in the app UI.

The app will be build with:

- docker(microservices)
- Django/DRF as backend (API)
- Swagger docs for API's
- Postgres as database for user and user saved links management
- Vue as frontend service
- Beautiful Soup for web scrapping

## Prerequistes:

1. Docker installed
2. Docker-compose installed (>= 3.5)


## Install codebase:

```
$ git clone https://github.com/anniejanuary/Real-Estate.git
```

## To run the app (while in project root):

1. Create .env (see .env_example) in project root
2. Start docker-compose to build services

```
$ docker-compose up -d --build
```

## Interaction with the app:

At this point following services availabe:

- Django API at localhost:8000/api
- Django admin panel available (log in after superuser creation) at localhost:8000/admin
- Vue frontend service available at localhost:8080
- PostgresDB operational for user save
<br>
Currently the app user can interact with the service thru either Vue front end service or Django based API.

For Vue frontend visit: localhost:8080
For API visit: localhost:8000/api/docs/

<br>

At this stage app user can:

- create new user
- log in
- get info about logged in user
- update logged in user (API only for now)

5. If any rebuild/ code change/ or db problems

```
$ docker-compose down -v
$ docker-compose up -d --build
```
<br>

### To add superuser (admin):

Firstly start the services (in order to apply migrations etc.)

```
$ docker-compose up
```
Then issue the command to create admin user:

```
$ docker-compose run --rm backend sh -c "python manage.py createsuperuser"
```

Finish user creation on interactive prompt and then you can login in onto service (users can be added, viewed, modified in admin dashboard - by Admin only) - with your credentials at:

<strong>localhost:8000/admin</strong>

<br>

## Testing

Tests made in Unittest.

Firsty database should be started if not already operational.

```
$ docker-compose up -d database
```
Tests should be ran thru docker-compose in order to get all needed django services started by manage.py.

Therefore:

- backend: a service name from docker-compose representing API service
- manage.py: django central file that tests are ran thru
- test: manage.py run all discovered tests within docker-compose workdir
- --rm switch: test container will be removed after test execution

```
$ docker-compose run --rm backend sh -c "python manage.py test"
```

Result will be produced in same terminal window after test execution.
For testing reference see: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing