# flask-template

## Required tools

`pyenv` - python version management

Linux:
https://github.com/pyenv/pyenv

Windows:
https://github.com/pyenv-win/pyenv-win

`poetry` - python dependency management and packaging 

https://python-poetry.org/docs/

## Getting started

### Install
`pyenv 3.8.0`
`pyenv local 3.8.0`
`poetry install`

### Run
`python app.py`

## Data flow

`HTTP request -> handler -> service -> handler -> HTTP response`

We use model classes to encapsulate data moving through the system. 
We use driver classes to initialize and maintain connection to external systems.

## Directory
`app.py` - main file, route declaration and drive and handler initialization

`/flask_template/driver` - A collection of classes that initiliazes communication with an external system (create of database connection, logging in to an external API)

`/flask_template/handler` - A collection of classes that deals receiving and parse of input from HTTP request

`/flask_template/service` - A collection of classes that deals with business logic

`/flask_template/model` - A collection of classes that serves as containers of data

## Dockerization