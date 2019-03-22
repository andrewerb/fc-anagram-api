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
python manage.py makemigrations
python manage.py migrate
```

We can now run the app if desired, but it's missing any data. So, the next step, then, is to populate the database with words from the included dictionary.txt

### Initalizing the Database

**PLEASE NOTE BEFORE THIS NEXT STEP**

Before proceeding, be aware that the initial database setup is ***slow***. The database is somewhat large, and it will take at least a few minutes to complete.

We can use a ready-made datadump (from a DB created from the text file in *data/*) as a [fixture](https://docs.djangoproject.com/en/2.1/howto/initial-data/) to setup the Django database. 

Navigate to the project's root directory, where *manage.py* is. If necessary, first review the database settings in *config/settings.py*. Use Django's manage.py **loaddata** command as follows.

```bash
python manage.py loaddata apps/wordapi/fixtures/wordapi_data.json
```

...And after several minutes, use runserver to start the database.

```bash
python manage.py runserver
```

The project should now be running, and should serve on http://127.0.0.1:8000/ by default. You're ready to query the API.

## API Usage

This app currently only supports GET methods. As this is a public API (for GET requiests, at least), methods take arguments via URL path and don't need additional parameters in their request. JSON API endpoints can be accessed at in the browser via their URL, in a web front-end, or pulled up through a program such as [HTTPie](https://httpie.org/).

The primary API methods are:

- Words by Substring-match
http://127.0.0.1:8000/api/substrings/substr

- Anagram by word label (the exact word itself)
http://127.0.0.1:8080/api/anagrams/label

- Anagrams of substring-match words\*
http://127.0.0.1:8080/api/substringanagrams/substr
\*Only first 10 results of anagrams sorted by 2nd character are returned.

(Insert whichever URL and port you're using to serve this project).

Only alpha characters will yield any results. For requests with no values found, or for input that isn't valid, expect a response with a **404** status, and the value:

```JSON
'None'
```

## Project Structure Overview

This is a pretty heavily abbreviated overview of the project directory structure:

```bash
fc_anagram_api
├── apps
│   └── wordapi
│       ├── ( *The API app* )
│       ├── apps.py
│       ├── management
│           └── commands
│               └── populate_db.py
│
├── config
│   └── ( *All of the settings stuff* )
├── data
│   └── dictionary.txt ( *For project initialization* )
├── manage.py
├── requirements.txt
```

In short, wordapi handles models, routing, views, and actual API responses for the Django project. Within that, management is where custom commands for manage.py are found. populate_db lives in that directory.

Config is where the project's settings and root urls.py are found.

data is where the dictionary.txt file is, read from populate_db.

## About

The objective of this project is to provide a way, via Django, to search the set of words in dictionary.txt (again, a file of 349,885 words), for words containing a given substring, and for matching anagrams within those words. Loading values into a database is an obvious and efficient way to handle such data. And as such, we can extend an API with that data.

This app's API methods are able to get:

- Words by *substring-matches* (words containing user-input as a substring)
- Anagram-words
- Anagram-words of substring matches\*

\***(In this project, only the first 10 anagram substring-matches are returned, from an overall set of anagram-words, sorted by their second character. This is as specified in the coding challenge.)**

This project relies on [Alphagrams](https://en.wiktionary.org/wiki/alphagram) as a means of matching words that are anagrams with one another. An alphagram is a sorted string of the same characters as its subject-word. Any words that are anagrams will share the same alphagram.

This project's data model represents this using Word, WordLanguage, and Alphagram objects. Anagrams are the result of a query of Words with a relationship to the same Alphagram object/value. There is also a WordDefinition model, though it is not used here. But more models and languages could be added with associations to words in data.

Substring matches are also found via queries in API views (controller).

Generic views (non-API endpoints) are also handled at this app's routing and views level, though that is something that might be best separated out if this project/API were extended.

### Futuere Optimizations

- **A production server**: The app will work better/faster off of SQLite3
- **Database initialization/population bulk-batching**: While this only slows the initial setup/installation process, it is not ideal for theoretical extension of this app for the onboarding of large new datasets to take so long. Bulk_create operations would definitely help, but the way in which Word models are saved needs refactoring. This is is referenced further in *apps/wordapi/models.py*.
- **Hardcoded anagram matches in data**: Would eliminate some queries but require more initialization overhead in data. It would just require more time to write the handlers for that ovehead.
- **A data model for small substring searches for word matches**, to optimize queries. Particularly useful for autofill-type behavior in the client.

At scale, a separate data model for hard-coded responses to smaller substring queries could even be offloaded to a separate database instance, separate app, and separate API. Ideally these could help scale for better concurrency to the client and end-user.

### Further Optimization and Enhancements

- In memory data store, such as Redis.
- Cloud server environment (such as AWS) for better scaled structuring, such as load balancers and database instances.
- Other API request methods and handling, outside of GET.
- Containerization, such as docker.
- Use of boilerplate project generation such as [Cookiecutter Django](https://github.com/pydanny/cookiecutter-django).
- Maybe a shorter README :)

### Other Things to Add

- Testing! Which was cut for time as of this commit.
- Further use and implementation of [Factory-Boy](https://github.com/FactoryBoy/factory_boy) for data testing
- An actual frontend.
- A live deployment for demoing.

While this wasn't my first project dealing with language or grammar, it was a relatively larger data-scale one, and an interesting one. I didn't now what *alphagrams* or *homographs* were prior, for instance. Further exploring data respresentations of words, language, translation would be an appealing undertaking.

## Favorite Sci-Fi movies

I couldn't see not answering this question, though it didn't exactly come up organically in my code comments anywhere (which are longer than what I often write as-is).

I often muse that my favorite sci-fi movie is the 2001 romcom, [Kate and Leopold](https://www.imdb.com/title/tt0035423/). This is typically just to invite someone to squabble with me over whether it is or is not sci-fi, to which I argue that it's a time-travel-centric story, and not a terrible one at that.

In truth, picking an actual favorite sci-fi movie is quite tricky. So, I made a list:

- The Iron Giant
- Wall-E
- Cowboy Bebop (The Movie, if it has to be a movie)
- Blade Runner 2049 (but obviously the original is a classic, of which I prefer The Final Cut)
- District 9
- Serenity/Firefly
- Children of Men
- The Matrix (which had **no sequels whatsoever**)
- Star Wars (but not most of that post-80s nonsense)
- Back to the Future (Part 2 and Part 3 are pretty good as long as you watch them in one sitting)
- Terminator 2 (which is a really wonderful example of color as a cinematic storytelling tool)
- Black Mirror (basically a movie anthology), not as much Bandersnatch though.

...And I am available to talk excessively at length about any/all of them.
