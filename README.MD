Install codebase:

git clone repo_link

Prerequistes:

1. Docker installed
2. Docker-compose installed

To run the app (while in project root):

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

Testing

Tests made in Unittest.

Test should be executed thru manage module - as django needs setup method to be fired in 
order to prepare all django modules/functions/elements to be available in test methods.
Therefore, while in terminal change path to folder where manage.py resides and then:

```
$ python manage.py test
```

Result will be produced in same terminal window after test execution.