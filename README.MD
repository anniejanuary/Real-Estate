Install codebase:

git clone repo_link

# Prerequistes:

1. Docker installed
2. Docker-compose installed

### To run the app (while in project root):

1. Create .env (see .env_example) in project root
2. Start docker

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
$ docker-compose run --rm web sh -c "python manage.py createsuperuser"
```

Finish user creation on interactive prompt and then you can login in into service (users can be added, viewed, modified in admin dashboard) - with your credentials at:

localhost:8000/admin


## Testing

Tests made in Unittest.

Firsty db should be started - or working containers (including db) should be up.

```
$ docker-compose up -d db
```
Tests should be ran thru docker-compose in order to get all needed django services.
Therefore:

- web: a service name from docker-compose
- manage.py: django central file that tests are ran thru
- core.tests: path for test catalogue in docker container
- --rm switch: test container will be removed after test execution

```
$ docker-compose run --rm web sh -c "python manage.py test core.tests"
```

Result will be produced in same terminal window after test execution.
For testing reference see: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing