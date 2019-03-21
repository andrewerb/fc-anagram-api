# Django Dictionary-Words / Anagram API

A web API in [Python 3](https://www.python.org), [Django](https://www.djangoproject.com), and [Django Rest Framework](https://www.django-rest-framework.org) for searching words and anagrams from a dictionary.

This project serves as a coding challenge submission by [Andrew Erb](http://andrewerb.com). The project takes a large dictionary-file of words, sorts them into a database, and provides a Python/Django API for requesting dictionary-word data.

## Getting started

### Requirements

- Python 3.7.2+ ...that's about it :)

This project is built in Python 3.7.2+, Django 2.1.7+, and Django Rest Framework 3.9.2+

Django and Django Rest can be installed via Pipenv.

To get the project going, the user needs to have at least Python 3.7. Pip is supported, but Pipenv (used for this project), or some form of version/package managers are encouraged. (Not everyone likes Pipenv. Poetry and PyEnv are other options that come highly recommended, but I haven't yet used them.)

This is very much a **dev** build of this project, and a proof of concept. So far, it's only deployed using Django's *runserver* command and SQLite3 as a DB. A production build of this project would need a production-ready server and database, such as PostgreSQL and Gunicorn.

It would not take much set up to change settings to use a more robust DB. Environment settings and allowed_hosts can be changed in this project's *settings.py* in the *config/* directory.

### Installation

To get started, download or git-clone this repo

```bash
git clone https://github.com/andrewerb/andrewerb.github.io.git
```

Install the required Python/Django dependencies, such as Django and Django Rest Framework

With Pipenv:

```bash
pipenv install
```

### Setup

Next steps are getting the database up and running and populating it with words from a large (349,885 line-items) dictionary-file, dictionary.txt in the *data/* directory.

To setup the Django database, navigate to the project's root directory. Use Django's manage.py migrate command to initialize our DB. This is best done after reviewing the database settings in *config/settings.py*

```bash
python manage.py makemigration
python manage.py migrate
```

We can now run the app if desired, but it's missing any data. So, the next step, then, is to populate the database with words from the included dictionary.txt

#### Initalizing the database

PLEASE NOTE BEFORE THIS NEXT STEP

Before proceeding, be aware that in its current iteration, the initial database setup is ***slow*** . It will take a few minutes to complete. (Notes on the issue with this design are expanded upon in apps/wordapi/models.py)

To proceed, use manage.py for this project's populate_db command.
\*(**Note:** avoid running this more than once as it currently lacks checks to keep it from redundant operations, and redundant Words are allowed by the data model.)

```bash
python manage.py populate_db
```

This command reads file in data/dictionary.txt

...After several minutes, use runserver to start the database.

```bash
python manage.py runserver
```

The project should now be serving on should serve on http://127.0.0.1:8000/ by default.

## About
TBC
