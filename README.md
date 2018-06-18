# Tangent Management System

A rest API driven management system to query and filter employee information.

### Prerequisites

1) You will need to clone this repo locally and cd into the tangent root folder.
2) You will need Python 2.7.9 and virtual env
3) You will need a virtual env setup , usually mkvirtualenv should do the trick , see http://docs.python-guide.org/en/latest/dev/virtualenvs/ for setup information.

## Getting Started

To install and run the application please do the following :
```
1) pip install -r requirements.txt
2) python manage.py migrate
3) python manage.py test       # Can do better, just an handful of tests
                               # due to time constraints.
4) Press CTRL + O in Google Chrome (or any other browser - may vary) and browse through
   to open this document => tangent/build/html/genindex.html , this help guide will provide full
   documentation on  most features of this app and help you understand the logic behind
   why and how this app was written. Please read through...
5) python manage.py runserver
6) visit : http://127.0.0.1:8000 and login with username and password provided.
```

### Folder structure
```
build -- This is where all the documentation for the app lives.
employees -- The APP that connects to the rest API and provides the features for
             searching and browsing employee information.
          -- templatetags - custom filter(s) to aid html formatting.
          -- views - All the backend views to respond to http requests.
screenshots -- Screenshots of what the admin dashboard looks like.
source -- Used by the document generator to compile the source help guide.
static -- assets
tangent -- The project settings , urls , wsgi file and so fourth.
tangent_core -- The API communication classes to convert the JSON API requests
                and responses to something the rest of our app can understand.
templates -- html template files.
```


### Why Python 2?

Well we should always use python 3 for new projects , however I've done something
crazy to my Ubuntu box and don't have the time to fiddle. So stuck with Python 2.7.9
for now , although most if not all of this code (probably not the urlencode stuff)
should work just fine with python 3.
