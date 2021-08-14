# Sandro API

This repo contains an example Flask application to provide a restful API that accepts XML content and
responds by calling other API's based on the content of the XML. Those other calls can be directed to
other sites with other response body types (JSON, XML, who knows)

# Installation

I used [pyenv](https://github.com/pyenv/pyenv) to create a Python VirtualEnv to run this application. I also had previously installed Python version 3.9.5, which I used here. This application should run without problems with not so current versions of Python

To install using pyenv follow these steps:

```console
git clone <this repository>
cd <cloned directory>
pyenv local 3.9.6
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

This will clone the repository into a directory, install a Python virtual environment in that directory, activate that virtual environment update the `pip` command and install the Python module requirements of the project.

# Running the application

You can run the app in a couple of ways, one using the Flask runner and the other with Gunicorn:

## Flask

This will run the application using the Flask development WSGI server, which works well for development, but
isn't suited for production.

```console
cd <where you cloned>/project
export FLASK_ENV=development
export FLASK_APP=rectangle.py
flask run
```

To exit CTRL-C

## Gunicorn

This will run the app with the Gunicorn WSGI server,
which is a good choice for production use (behind a web server like Nginx or Apache). The command below will run 4 workers. There are other options as well to optimize how the app is run.

```console
cd <where you cloned>/project
gunicorn -w 4 "rectangle:create_app()"
```

To exit CTRL-C

# Using The Application

Once the app is running you can browse to it at the localhost url, something like `localhost:5000` if run with Flask. If you use Gunicorn browse to it at
`localhost:8000`.

This will bring up a regular web server page in the browser just to show you it's working. Use something like Postman to make requests to the API.

Here is the XML payload to POST to the API. You can modify this as you see fit. The `note` field is included here, but only required/used in the V1 version of the API.

```xml
<payment>
<patient>
<first_name>Tom</first_name>
<last_name>Wilson</last_name>
</patient>
<amount>37.45</amount>
<note>Paid in Cash</note>
</payment>
```

The API supports 2 versions, v1 and v2 and there are two merchants in the database, 1 and 2. Here are the URL endpoints supported:

* localhost:5000/api/v1/1/payment
* localhost:5000/api/v1/2/payment
* localhost:5000/api/v2/1/payment
* localhost:5000/api/v1/2/payment

# Notes

The system includes an initialized SQLite database, rectangle.sqlite. You can erase and rebuild this (with data) by running these commands:

```console
cd cd <where you cloned>/project
python init_db.py
```

The application only has some error handling and no validation of incoming or outgoing information.

The system uses Flask Blueprints to provide the API URL endpoints for the versions. It also has some factory classes to provide creators for the merchants and payment managers. 