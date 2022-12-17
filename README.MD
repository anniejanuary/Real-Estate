# General info

<strong>THE APP in first stage of development. Backend/ frontend services under construction.</strong>

Django/ Vue web app for gathering real estate announces form various web sites in order to present result to the user accordingly to his criteria in the app UI.

The app will be build with:

- dockerized microservices
- Django/DRF backend (API)
- Postgres as database
- Vue as frontend service
- Beautiful Soup for web scrapping

## Prerequistes:

1. Docker installed
2. Docker-compose installed (>= 3.5)


### Install codebase:

```
$ git clone https://github.com/anniejanuary/Real-Estate.git
```

### To run the app (while in project root):

1. Create .env (see .env_example) in project root
2. Start docker-compose to build services

```
$ docker-compose up -d --build
```

3. Go to: localhost:8000 for Django status page
4. If any rebuild/ code change/ or db problem

```
$ docker-compose down -v
$ docker-compose up -d --build
```

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

localhost:8000/admin


## Testing

Tests made in Unittest.

Firsty database should be started if not already operational.

```
$ docker-compose up -d database
```
Tests should be ran thru docker-compose in order to get all needed django services started by manage.py.

Therefore:

- backend: a service name from docker-compose
- manage.py: django central file that tests are ran thru
- core.tests: path for test catalogue in docker container
- --rm switch: test container will be removed after test execution

```
$ docker-compose run --rm backend sh -c "python manage.py test core.tests"
```

Result will be produced in same terminal window after test execution.
For testing reference see: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing